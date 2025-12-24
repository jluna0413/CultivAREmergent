import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.commission_service import CommissionService
from datetime import datetime, timedelta

@pytest.mark.asyncio
async def test_get_daily_sales_history():
    # Mock DB Session
    mock_db = AsyncMock()
    
    # Mock Result Rows
    # Day 1: $100, 2 sales (Yesterday)
    # Day 2: $50, 1 sale (Today)
    now = datetime.utcnow()
    day1 = (now - timedelta(days=1)).date()
    day2 = now.date()
    
    mock_row1 = MagicMock()
    mock_row1.day = day1
    mock_row1.total = 100.0
    mock_row1.count = 2
    
    mock_row2 = MagicMock()
    mock_row2.day = day2
    mock_row2.total = 50.0
    mock_row2.count = 1
    
    mock_result = MagicMock()
    mock_result.all.return_value = [mock_row1, mock_row2]
    mock_db.execute.return_value = mock_result
    
    # Run Service
    history = await CommissionService.get_daily_sales_history(mock_db, breeder_user_id=1, days=3)
    
    # Assertions
    assert len(history) == 3 # Requested 3 days
    
    # Day 0 (Today) matches mock_row2
    assert history[-1]["date"] == str(day2)
    assert history[-1]["amount"] == 50.0
    
    # Day -1 (Yesterday) matches mock_row1
    assert history[-2]["date"] == str(day1)
    assert history[-2]["amount"] == 100.0
    
    # Day -2 (2 days ago) should be 0 (Empty fill)
    empty_day = (now - timedelta(days=2)).date()
    assert history[-3]["date"] == str(empty_day)
    assert history[-3]["amount"] == 0.0
