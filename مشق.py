import random
import time
import pandas as pd
import pingouin as pg

random.seed(42)
N_PER_GROUP = 100   # تعداد مشاهده در هر گروه (برای کل داده‌ها: 300)
REPEATS = 200       # تعداد تکرار برای میانگین‌گیری زمان



def wage_generator(n, mu, sigma):
    for _ in range(n):
        yield round(random.gauss(mu, sigma), 1)


names = ["industry", "services", "agriculture"]
wages = {
    "industry":    list(wage_generator(N_PER_GROUP, 57, 4)),
    "services":    list(wage_generator(N_PER_GROUP, 54, 4)),
    "agriculture": list(wage_generator(N_PER_GROUP, 39, 4)),
}


# fallah
def manual_anova(wages, names):
    all_vals = []
    for name in names:
        for val in wages[name]:
            all_vals.append(val)

    total = len(all_vals)
    X_bar = sum(all_vals) / total

    ssb = 0
    for name in names:
        group = wages[name]
        n_j = len(group)
        X_bar_j = sum(group) / n_j
        ssb += n_j * (X_bar_j - X_bar) ** 2

    ssw = 0
    for name in names:
        group = wages[name]
        X_bar_j = sum(group) / len(group)
        for val in group:
            ssw += (val - X_bar_j) ** 2

    k = len(names)
    df_b = k - 1
    df_w = total - k
    msb = ssb / df_b
    msw = ssw / df_w
    return ssb, ssw, msb, msw, msb / msw


# my way
def pingouin_anova(wages, names):
    df = pd.DataFrame([(n, x) for n in names for x in wages[n]],
                      columns=["sector", "wage"])
    table = pg.anova(data=df, dv="wage", between="sector", detailed=True)
    ssb, ssw = table["SS"]
    msb, msw = table["MS"]
    return ssb, ssw, msb, msw, table.loc[0, "F"]



def bench(func, repeats):
    func(wages, names)  
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        func(wages, names)
        times.append(time.perf_counter() - t0)
    return sum(times) / len(times), min(times)


res_manual = manual_anova(wages, names)
res_ping = pingouin_anova(wages, names)
print("F دستی     =", res_manual[-1])
print("F pingouin =", res_ping[-1])

avg_m, min_m = bench(manual_anova, REPEATS)
avg_p, min_p = bench(pingouin_anova, REPEATS)

print(f"\nدستی    : میانگین = {avg_m*1000:.4f} ms | کمترین = {min_m*1000:.4f} ms")
print(f"pingouin: میانگین = {avg_p*1000:.4f} ms | کمترین = {min_p*1000:.4f} ms")
print(f"نسبت (pingouin / دستی) = {avg_p / avg_m:.1f} برابر")