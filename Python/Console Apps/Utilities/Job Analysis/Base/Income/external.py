"""External income inputs. Personal amounts stay in local environment variables."""

import os

cash_on_hand = float(input("Cash: "))
current_savings = float(os.environ.get("JOB_ANALYSIS_CURRENT_SAVINGS", "0") or 0)
