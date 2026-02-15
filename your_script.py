import pandas as pd
import os

# create folders if not exist
os.makedirs("output", exist_ok=True)
os.makedirs("profiling", exist_ok=True)

# =========================
# LOAD DATA
# =========================

lead_logs = pd.read_csv("data/lead_log.csv")
paid_transactions = pd.read_csv("data/paid_transactions.csv")
referral_rewards = pd.read_csv("data/referral_rewards.csv")
user_logs = pd.read_csv("data/user_logs.csv")
user_referral_logs = pd.read_csv("data/user_referral_logs.csv")
user_referral_statuses = pd.read_csv("data/user_referral_statuses.csv")
user_referrals = pd.read_csv("data/user_referrals.csv")

# =========================
# DATA PROFILING
# =========================

def profile_table(df, name):
    return pd.DataFrame({
        "table": name,
        "column": df.columns,
        "null_count": df.isnull().sum().values,
        "distinct_count": df.nunique().values
    })

profile = pd.concat([
    profile_table(lead_logs, "lead_logs"),
    profile_table(paid_transactions, "paid_transactions"),
    profile_table(referral_rewards, "referral_rewards"),
    profile_table(user_logs, "user_logs"),
    profile_table(user_referral_logs, "user_referral_logs"),
    profile_table(user_referral_statuses, "user_referral_statuses"),
    profile_table(user_referrals, "user_referrals")
])

profile.to_csv("profiling/data_profile.csv", index=False)

print("Data profiling completed.")

# =========================
# DATA CLEANING
# =========================

# convert datetime columns safely
date_columns = [
    "referral_at",
    "updated_at",
    "created_at",
    "transaction_at"
]

for col in date_columns:
    if col in user_referrals.columns:
        user_referrals[col] = pd.to_datetime(user_referrals[col], errors="coerce")

    if col in paid_transactions.columns:
        paid_transactions[col] = pd.to_datetime(paid_transactions[col], errors="coerce")

# convert reward_value to numeric
if "reward_value" in referral_rewards.columns:
    referral_rewards["reward_value"] = pd.to_numeric(referral_rewards["reward_value"], errors="coerce")

# =========================
# JOIN TABLES (FIXED VERSION)
# =========================

# rename columns to avoid conflict
user_logs = user_logs.rename(columns={"id": "user_log_id"})
user_referral_statuses = user_referral_statuses.rename(columns={"id": "status_id"})
referral_rewards = referral_rewards.rename(columns={"id": "reward_id"})
user_referral_logs = user_referral_logs.rename(columns={"id": "referral_log_id"})

# merge referrer info
df = user_referrals.merge(
    user_logs,
    left_on="referrer_id",
    right_on="user_id",
    how="left"
)

# merge referral status
df = df.merge(
    user_referral_statuses,
    left_on="user_referral_status_id",
    right_on="status_id",
    how="left"
)

# merge reward info
df = df.merge(
    referral_rewards,
    left_on="referral_reward_id",
    right_on="reward_id",
    how="left"
)

# merge transaction info
df = df.merge(
    paid_transactions,
    on="transaction_id",
    how="left"
)

# merge referral logs
df = df.merge(
    user_referral_logs,
    left_on="referral_id",
    right_on="user_referral_id",
    how="left"
)

# =========================
# BUSINESS LOGIC
# =========================

df["is_business_logic_valid"] = False

valid_condition = (
    (df["reward_value"] > 0) &
    (df["description"] == "Berhasil") &
    (df["transaction_status"] == "PAID") &
    (df["transaction_type"] == "NEW")
)

df.loc[valid_condition, "is_business_logic_valid"] = True

# =========================
# SELECT FINAL COLUMNS
# =========================

final_columns = [
    "referral_id",
    "referral_at",
    "referrer_id",
    "referee_name",
    "referee_phone",
    "description",
    "reward_value",
    "transaction_id",
    "transaction_status",
    "transaction_at",
    "transaction_location",
    "transaction_type",
    "is_business_logic_valid"
]

final_df = df[final_columns].drop_duplicates()

# =========================
# SAVE OUTPUT
# =========================

final_df.to_csv("output/referral_report.csv", index=False)

print("Final report generated in output/referral_report.csv")
