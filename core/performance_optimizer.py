"""
性能优化模块
缓存机制 + 并发优化 + API性能提升

创建时间：2026-05-01 22:15
版本：v1.0
开发者：天工Agent + 磐石Agent
"""

from datetime import datetime, timedelta
from typing import Dict, Optional, Any
import json
import hashlib
import asyncio
from functools import wraps

# ============================================
# 缓存机制 ⭐⭐⭐⭐⭐
# ============================================

class CacheManager:
    """缓存管理器（内存缓存）"""
    
    def __init__(self, max_size: int = 1000, default_ttl: int = 3600):
        """
        初始化缓存管理器
        
        Args:
            max_size: 最大缓存条数
            default_ttl: 默认过期时间（秒）
        """
        self.cache = {}  # 缓存数据
        self.max_size = max_size
        self.default_ttl = default_ttl
    
    def _generate_key(self, key_data: Any) -> str:
        """生成缓存键"""
        if isinstance(key_data, str):
            return key_data
        
        # 将复杂对象转为JSON字符串，再哈希
        json_str = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(json_str.encode()).hexdigest()
    
    def get(self, key: Any) -> Optional[Any]:
        """
        获取缓存数据
        
        Args:
            key: 缓存键
        
        Returns:
            Optional[Any]: 缓存数据（不存在或过期返回None）
        """
        cache_key = self._generate_key(key)
        
        if cache_key not in self.cache:
            return None
        
        cache_entry = self.cache[cache_key]
        
        # 检查过期时间 ⭐⭐⭐⭐⭐
        if datetime.now() > cache_entry["expires_at"]:
            del self.cache[cache_key]
            return None
        
        return cache_entry["data"]
    
    def set(
        self,
        key: Any,
        value: Any,
        ttl: Optional[int] = None,
    ) -> bool:
        """
        设置缓存数据
        
        Args:
            key: 缓存键
            value: 缓存数据
            ttl: 过期时间（秒）
        
        Returns:
            bool: 设置是否成功
        """
        cache_key = self._generate_key(key)
        
        # 检查缓存大小 ⭐⭐⭐⭐⭐
        if len(self.cache) >= self.max_size:
            # 清理过期缓存
            self._clean_expired()
            
            # 如果仍超过限制，删除最旧的缓存
            if len(self.cache) >= self.max_size:
                oldest_key = min(
                    self.cache.keys(),
                    key=lambda k: self.cache[k]["created_at"]
                )
                del self.cache[oldest_key]
        
        # 设置缓存 ⭐⭐⭐⭐⭐
        expires_at = datetime.now() + timedelta(seconds=ttl or self.default_ttl)
        
        self.cache[cache_key] = {
            "data": value,
            "created_at": datetime.now(),
            "expires_at": expires_at,
        }
        
        return True
    
    def delete(self, key: Any) -> bool:
        """
        删除缓存数据
        
        Args:
            key: 缓存键
        
        Returns:
            bool: 删除是否成功
        """
        cache_key = self._generate_key(key)
        
        if cache_key in self.cache:
            del self.cache[cache_key]
            return True
        
        return False
    
    def clear(self) -> bool:
        """清空缓存"""
        self.cache.clear()
        return True
    
    def _clean_expired(self) -> int:
        """清理过期缓存"""
        expired_keys = [
            k for k, v in self.cache.items()
            if datetime.now() > v["expires_at"]
        ]
        
        for key in expired_keys:
            del self.cache[key]
        
        return len(expired_keys)
    
    def get_stats(self) -> Dict:
        """获取缓存统计"""
        self._clean_expired()
        
        return {
            "total_entries": len(self.cache),
            "max_size": self.max_size,
            "default_ttl": self.default_ttl,
        }

# ============================================
# 预警缓存装饰器 ⭐⭐⭐⭐⭐
# ============================================

# 全局缓存管理器
warning_cache = CacheManager(max_size=500, default_ttl=1800)  # 30分钟缓存 ⭐⭐⭐⭐⭐

def cached_warning(ttl: int = 1800):
    """
    预警缓存装饰器
    
    Args:
        ttl: 缓存过期时间（秒）
    
    Returns:
        decorator: 装饰器函数
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存键（基于函数名 + 参数）⭐⭐⭐⭐⭐
            cache_key = {
                "func_name": func.__name__,
                "args": args,
                "kwargs": kwargs,
            }
            
            # 尝试从缓存获取 ⭐⭐⭐⭐⭐
            cached_result = warning_cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # 执行函数 ⭐⭐⭐⭐⭐
            result = func(*args, **kwargs)
            
            # 缓存结果 ⭐⭐⭐⭐⭐
            warning_cache.set(cache_key, result, ttl)
            
            return result
        
        return wrapper
    
    return decorator

# ============================================
# 并发优化 ⭐⭐⭐⭐⭐
# ============================================

class AsyncTaskManager:
    """异步任务管理器"""
    
    def __init__(self, max_concurrent: int = 10):
        """
        初始化异步任务管理器
        
        Args:
            max_concurrent: 最大并发数
        """
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def run_task(
        self,
        task_func: callable,
        task_args: tuple = (),
        task_kwargs: dict = {},
    ) -> Any:
        """
        运行异步任务
        
        Args:
            task_func: 任务函数
            task_args: 任务参数
            task_kwargs: 任务关键字参数
        
        Returns:
            Any: 任务结果
        """
        async with self.semaphore:
            # 执行任务 ⭐⭐⭐⭐⭐
            if asyncio.iscoroutinefunction(task_func):
                result = await task_func(*task_args, **task_kwargs)
            else:
                result = task_func(*task_args, **task_kwargs)
            
            return result
    
    async def run_batch_tasks(
        self,
        task_func: callable,
        task_args_list: list,
    ) -> list:
        """
        批量运行异步任务
        
        Args:
            task_func: 任务函数
            task_args_list: 任务参数列表
        
        Returns:
            list: 任务结果列表
        """
        tasks = [
            self.run_task(task_func, args)
            for args in task_args_list
        ]
        
        # 并发执行 ⭐⭐⭐⭐⭐
        results = await asyncio.gather(*tasks)
        
        return results

# ============================================
# API性能优化 ⭐⭐⭐⭐⭐
# ============================================

class APIPerformanceOptimizer:
    """API性能优化器"""
    
    def __init__(self):
        self.request_stats = {}  # 请求统计
        self.batch_size = 10  # 批量处理大小
    
    def record_request(
        self,
        api_endpoint: str,
        response_time: float,
        success: bool,
    ) -> Dict:
        """
        记录API请求
        
        Args:
            api_endpoint: API端点
            response_time: 响应时间（秒）
            success: 是否成功
        
        Returns:
            Dict: 请求统计
        """
        if api_endpoint not in self.request_stats:
            self.request_stats[api_endpoint] = {
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0,
                "total_response_time": 0,
                "avg_response_time": 0,
                "max_response_time": 0,
                "min_response_time": float('inf'),
            }
        
        stats = self.request_stats[api_endpoint]
        stats["total_requests"] += 1
        
        if success:
            stats["successful_requests"] += 1
        else:
            stats["failed_requests"] += 1
        
        stats["total_response_time"] += response_time
        stats["avg_response_time"] = stats["total_response_time"] / stats["total_requests"]
        
        if response_time > stats["max_response_time"]:
            stats["max_response_time"] = response_time
        
        if response_time < stats["min_response_time"]:
            stats["min_response_time"] = response_time
        
        return stats
    
    def get_api_stats(self) -> Dict:
        """获取API统计"""
        return self.request_stats
    
    def optimize_batch_requests(
        self,
        requests: list,
    ) -> list:
        """
        优化批量请求
        
        Args:
            requests: 请求列表
        
        Returns:
            list: 分批后的请求列表
        """
        # 分批处理 ⭐⭐⭐⭐⭐
        batches = []
        
        for i in range(0, len(requests), self.batch_size):
            batch = requests[i:i + self.batch_size]
            batches.append(batch)
        
        return batches

# ============================================
# 性能监控 ⭐⭐⭐⭐⭐
# ============================================

class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self):
        self.metrics = {}  # 性能指标
    
    def record_metric(
        self,
        metric_name: str,
        value: float,
        timestamp: Optional[datetime] = None,
    ) -> Dict:
        """
        记录性能指标
        
        Args:
            metric_name: 指标名称
            value: 指标值
            timestamp: 时间戳
        
        Returns:
            Dict: 指标数据
        """
        if metric_name not in self.metrics:
            self.metrics[metric_name] = []
        
        metric_entry = {
            "value": value,
            "timestamp": timestamp or datetime.now(),
        }
        
        self.metrics[metric_name].append(metric_entry)
        
        return metric_entry
    
    def get_metric_stats(
        self,
        metric_name: str,
        limit: int = 100,
    ) -> Dict:
        """
        获取指标统计
        
        Args:
            metric_name: 指标名称
            limit: 限制数量
        
        Returns:
            Dict: 指标统计
        """
        if metric_name not in self.metrics:
            return {}
        
        metric_values = [
            m["value"]
            for m in self.metrics[metric_name][-limit:]
        ]
        
        if len(metric_values) == 0:
            return {}
        
        return {
            "count": len(metric_values),
            "avg": sum(metric_values) / len(metric_values),
            "max": max(metric_values),
            "min": min(metric_values),
            "latest": metric_values[-1],
        }
    
    def get_all_metrics(self) -> Dict:
        """获取所有指标"""
        return self.metrics

# ============================================
# API接口 ⭐⭐⭐⭐⭐
# ============================================

# 全局实例
cache_manager = CacheManager()
async_task_manager = AsyncTaskManager()
api_optimizer = APIPerformanceOptimizer()
performance_monitor = PerformanceMonitor()

def cache_get_api(key: str) -> Dict:
    """缓存获取API"""
    result = cache_manager.get(key)
    
    return {
        "key": key,
        "found": result is not None,
        "data": result,
    }

def cache_set_api(
    key: str,
    value: Any,
    ttl: Optional[int] = None,
) -> Dict:
    """缓存设置API"""
    success = cache_manager.set(key, value, ttl)
    
    return {
        "key": key,
        "success": success,
    }

def cache_stats_api() -> Dict:
    """缓存统计API"""
    stats = cache_manager.get_stats()
    
    return stats

def api_stats_api() -> Dict:
    """API统计API"""
    stats = api_optimizer.get_api_stats()
    
    return stats

def performance_stats_api(metric_name: Optional[str] = None) -> Dict:
    """性能统计API"""
    if metric_name:
        return performance_monitor.get_metric_stats(metric_name)
    
    return performance_monitor.get_all_metrics()

# ============================================
# 测试
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("性能优化模块测试")
    print("=" * 60)
    
    # 测试缓存
    cache_result = cache_set_api("test_key", {"data": "test_value"}, ttl=60)
    print(f"缓存设置结果：{cache_result}")
    
    cache_get_result = cache_get_api("test_key")
    print(f"缓存获取结果：{cache_get_result}")
    
    # 测试缓存统计
    stats_result = cache_stats_api()
    print(f"缓存统计：{stats_result}")
    
    # 测试API性能记录
    api_optimizer.record_request("/api/v1/warning/generate", 0.5, True)
    api_optimizer.record_request("/api/v1/warning/generate", 0.3, True)
    api_optimizer.record_request("/api/v1/warning/generate", 0.8, False)
    
    api_stats = api_stats_api()
    print(f"API统计：{api_stats}")
    
    # 测试性能监控
    performance_monitor.record_metric("response_time", 0.5)
    performance_monitor.record_metric("response_time", 0.3)
    performance_monitor.record_metric("response_time", 0.7)
    
    perf_stats = performance_stats_api("response_time")
    print(f"性能统计：{perf_stats}")
    
    print("=" * 60)