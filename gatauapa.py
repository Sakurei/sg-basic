import pandas as pd
from datetime import date, timedelta

# 1) Load anggota
df_members = pd.read_csv("members.csv")
required_divisions = [
    "internal SDM",
    "internal logistik",
    "eksternal",
    "chameleon",
    "Daruma",
    "NBBDC",
    "DnA",
    "Honnoukai",
    "TnT",
]

start_date = date(2026, 1, 5)  # periode 1 mulai
periods = 6                    # mau berapa periode (1 periode = 14 hari)

all_periods = []
for p in range(1, periods + 1):
    start = start_date + timedelta(days=(p - 1) * 14)
    end = start + timedelta(days=13)

    # validasi divisi wajib
    missing = sorted(set(required_divisions) - set(df_members["divisi"].unique()))
    if missing:
        raise ValueError(f"Divisi ini belum ada anggotanya di members.csv: {missing}")

    # filter hanya divisi yang dipakai, lalu ambil 1 random per divisi
    df_pick = (
        df_members[df_members["divisi"].isin(required_divisions)]
        .groupby("divisi", group_keys=False)
        .sample(n=1, random_state=100 + p)   # beda seed tiap periode [web:1414]
        .sort_values("divisi")
        .reset_index(drop=True)
    )

    df_pick.insert(0, "Periode", p)
    df_pick.insert(1, "Mulai", start.isoformat())
    df_pick.insert(2, "Sampai", end.isoformat())
    all_periods.append(df_pick)

df_schedule = pd.concat(all_periods, ignore_index=True)

# tampilkan tabel
print(df_schedule.to_string(index=False))
