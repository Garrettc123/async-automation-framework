#!/usr/bin/env python3
"""
Enhanced Quantum Revenue Engine with Retry Logic and Error Handling
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Optional, List
from enum import Enum
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("QuantumRevenueEngine")

class StreamStatus(Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    ERROR = "error"
    RECOVERING = "recovering"

class RevenueStream:
    """Individual revenue stream with retry and backoff logic"""
    
    def __init__(self, name: str, max_retries: int = 3):
        self.name = name
        self.status = StreamStatus.ACTIVE
        self.max_retries = max_retries
        self.retry_count = 0
        self.total_processed = 0
        self.total_errors = 0
        self.last_error = None
        self.last_success = None
        
    async def process_event(self) -> bool:
        """Process revenue event with retry logic"""
        retry_delay = 1
        
        for attempt in range(self.max_retries):
            try:
                # Simulate processing
                await asyncio.sleep(0.5)
                
                # Simulate 5% failure rate
                if random.random() < 0.05:
                    raise Exception("Simulated processing failure")
                    
                # Success
                self.total_processed += 1
                self.last_success = datetime.now()
                self.status = StreamStatus.ACTIVE
                self.retry_count = 0
                
                logger.info(f"[{self.name}] Event processed successfully (Total: {self.total_processed})")
                return True
                
            except Exception as e:
                self.retry_count = attempt + 1
                self.total_errors += 1
                self.last_error = str(e)
                
                if attempt < self.max_retries - 1:
                    logger.warning(f"[{self.name}] Attempt {attempt + 1} failed: {e}. Retrying in {retry_delay}s...")
                    self.status = StreamStatus.RECOVERING
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    logger.error(f"[{self.name}] All retry attempts failed: {e}")
                    self.status = StreamStatus.ERROR
                    
        return False
        
    def get_metrics(self) -> Dict:
        """Get stream metrics"""
        return {
            'name': self.name,
            'status': self.status.value,
            'total_processed': self.total_processed,
            'total_errors': self.total_errors,
            'retry_count': self.retry_count,
            'last_error': self.last_error,
            'last_success': self.last_success.isoformat() if self.last_success else None,
            'success_rate': (self.total_processed / (self.total_processed + self.total_errors) * 100) 
                           if (self.total_processed + self.total_errors) > 0 else 0
        }

class QuantumRevenueEngine:
    """Enhanced revenue engine with comprehensive error handling"""
    
    def __init__(self):
        self.streams = [
            RevenueStream("Stripe Subscriptions"),
            RevenueStream("PayPal One-Time"),
            RevenueStream("Crypto Payments"),
            RevenueStream("Wire Transfers"),
            RevenueStream("Affiliate Revenue")
        ]
        self.is_running = True
        self.webhook_queue = asyncio.Queue(maxsize=1000)
        self.total_revenue = 0.0
        self.start_time = datetime.now()
        
    async def process_stream(self, stream: RevenueStream):
        """Process events for a single revenue stream"""
        while self.is_running:
            try:
                if stream.status != StreamStatus.PAUSED:
                    await stream.process_event()
                    
                # Simulate revenue
                revenue = random.uniform(10, 1000)
                self.total_revenue += revenue
                
                # Wait before next event
                await asyncio.sleep(random.uniform(3, 8))
                
            except asyncio.CancelledError:
                logger.info(f"[{stream.name}] Processing cancelled")
                break
            except Exception as e:
                logger.error(f"[{stream.name}] Unexpected error: {e}")
                stream.status = StreamStatus.ERROR
                await asyncio.sleep(5)
                
    async def payment_webhook_listener(self):
        """Enhanced webhook listener with queue processing"""
        while self.is_running:
            try:
                logger.info(f"Webhook listener active (Queue size: {self.webhook_queue.qsize()})")
                
                # Simulate incoming webhooks
                if random.random() < 0.3:  # 30% chance of webhook
                    webhook_data = {
                        'type': random.choice(['payment.success', 'payment.failed', 'subscription.renewed']),
                        'amount': random.uniform(10, 500),
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    try:
                        self.webhook_queue.put_nowait(webhook_data)
                        logger.info(f"Webhook received: {webhook_data['type']}")
                    except asyncio.QueueFull:
                        logger.warning("Webhook queue full - dropping event")
                        
                # Process queued webhooks
                if not self.webhook_queue.empty():
                    webhook = await self.webhook_queue.get()
                    logger.info(f"Processing webhook: {webhook['type']} - ${webhook['amount']:.2f}")
                    self.webhook_queue.task_done()
                    
                await asyncio.sleep(5)
                
            except asyncio.CancelledError:
                logger.info("Webhook listener cancelled")
                break
            except Exception as e:
                logger.error(f"Webhook listener error: {e}")
                await asyncio.sleep(5)
                
    async def get_system_metrics(self) -> Dict:
        """Get comprehensive system metrics"""
        uptime = (datetime.now() - self.start_time).total_seconds()
        
        return {
            'uptime_seconds': uptime,
            'total_revenue': self.total_revenue,
            'revenue_per_second': self.total_revenue / uptime if uptime > 0 else 0,
            'webhook_queue_size': self.webhook_queue.qsize(),
            'streams': [stream.get_metrics() for stream in self.streams],
            'timestamp': datetime.now().isoformat()
        }
        
    async def health_check(self) -> bool:
        """Check overall system health"""
        error_streams = sum(1 for s in self.streams if s.status == StreamStatus.ERROR)
        total_streams = len(self.streams)
        
        health = error_streams < (total_streams * 0.5)  # Less than 50% in error
        
        if not health:
            logger.warning(f"System unhealthy: {error_streams}/{total_streams} streams in ERROR state")
            
        return health
        
    async def print_metrics(self):
        """Print metrics periodically"""
        while self.is_running:
            try:
                metrics = await self.get_system_metrics()
                
                print("\n" + "="*60)
                print(f"QUANTUM REVENUE ENGINE METRICS")
                print("="*60)
                print(f"Total Revenue: ${metrics['total_revenue']:.2f}")
                print(f"Revenue/sec: ${metrics['revenue_per_second']:.2f}")
                print(f"Webhook Queue: {metrics['webhook_queue_size']}")
                print(f"Uptime: {metrics['uptime_seconds']:.0f}s")
                print("\nStream Status:")
                
                for stream in metrics['streams']:
                    status_icon = {
                        'active': '✓',
                        'error': '✗',
                        'recovering': '⟳',
                        'paused': '⏸'
                    }.get(stream['status'], '?')
                    
                    print(f"  {status_icon} {stream['name']:<25} "
                          f"Processed: {stream['total_processed']:<5} "
                          f"Errors: {stream['total_errors']:<3} "
                          f"Success: {stream['success_rate']:.1f}%")
                          
                print("="*60 + "\n")
                
                await asyncio.sleep(15)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Metrics printing error: {e}")
                await asyncio.sleep(15)
                
    async def start(self):
        """Start the quantum revenue engine"""
        logger.info("="*60)
        logger.info("STARTING ENHANCED QUANTUM REVENUE ENGINE")
        logger.info("="*60)
        
        # Create tasks for each stream
        tasks = [asyncio.create_task(self.process_stream(stream)) for stream in self.streams]
        
        # Add webhook listener
        tasks.append(asyncio.create_task(self.payment_webhook_listener()))
        
        # Add metrics printer
        tasks.append(asyncio.create_task(self.print_metrics()))
        
        try:
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            logger.info("Engine shutdown requested")
        finally:
            self.is_running = False
            logger.info("Quantum Revenue Engine stopped")
            
    async def graceful_shutdown(self):
        """Gracefully shutdown the engine"""
        logger.info("Initiating graceful shutdown...")
        self.is_running = False
        
        # Wait for webhook queue to empty
        if not self.webhook_queue.empty():
            logger.info(f"Draining webhook queue ({self.webhook_queue.qsize()} remaining)...")
            await self.webhook_queue.join()
            
        # Print final metrics
        metrics = await self.get_system_metrics()
        logger.info(f"Final Revenue: ${metrics['total_revenue']:.2f}")
        logger.info("Shutdown complete")

if __name__ == "__main__":
    engine = QuantumRevenueEngine()
    try:
        asyncio.run(engine.start())
    except KeyboardInterrupt:
        logger.info("Shutdown signal received")
