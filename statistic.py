import math
import statistics


print("\n==========tamrin_aval==========")

spending = [46.0, 47.7, 43.4, 49.3, 46.5,
            45.1, 48.8, 42.9, 48.1, 45.3, 46.9, 44.4]

mu0 = 45


def t_one_sample(data, mu0):
    n = len(data)
    mean = statistics.mean(data)
    s = statistics.stdev(data)

    t = (mean - mu0) / (s / math.sqrt(n))

    return t


t = t_one_sample(spending, mu0)

print("t =", t)

if abs(t) > 2.201:
    print("farz 0 rad mishavad")
else:
    print("farz 0 rad nemishavad")


print("\n==========tamrin_dovom==========")

salary = {
    "tehran": [38.5, 42.0, 35.8, 40.2, 44.1, 37.6, 41.3, 39.9, 43.5, 36.7],

    "isfahan": [35.7, 39.0, 34.3, 40.5, 36.9, 37.6, 33.4, 39.7, 35.1, 37.3, 38.5, 36.0]
}

x = salary["tehran"]
y = salary["isfahan"]

print("Mean Tehran:", statistics.mean(x))
print("Mean Isfahan:", statistics.mean(y))


def t_two_sample(x, y):
    n1 = len(x)
    n2 = len(y)

    mean1 = statistics.mean(x)
    mean2 = statistics.mean(y)

    s1 = statistics.variance(x)
    s2 = statistics.variance(y)

    sp = math.sqrt(((n1-1)*s1 + (n2-1)*s2) / (n1+n2-2))

    t = (mean1 - mean2) / (sp * math.sqrt(1/n1 + 1/n2))

    return t


t = t_two_sample(x, y)

print("t =", t)


if abs(t) > 2.086:
    print("farz 0 rad mishavad")
else:
    print("farz 0 rad nmishavad")


if t > 1.725:
    print("miangin hoghough tehran bishtar ast")
else:
    print("shavahed kafi nadarim")


print("\n==========tamrin_sevom==========")


sales = {
    "before": [120, 85, 210, 150, 95, 175, 60, 240, 130, 110],

    "after": [126, 90, 214, 158, 98, 183, 63, 247, 134, 118]
}

diff = []

for i in range(len(sales["before"])):
    diff.append(sales["after"][i] - sales["before"][i])

print("Differences:", diff)


def t_one_sample(data, mu0):
    n = len(data)

    mean = statistics.mean(data)
    s = statistics.stdev(data)

    t = (mean - mu0) / (s / math.sqrt(n))

    return t


t = t_one_sample(diff, 0)

print("t =", t)

if t > 1.833:
    print("farz 0 rad mishavad")
else:
    print("farz 0 rad nemishavad")


print("\n==========tamrin_chaharom==========")

wages = {
    "industry": [52, 58, 61, 55, 63, 57],

    "services": [49, 54, 60, 51, 56, 53],

    "agriculture": [38, 42, 35, 45, 40, 36]
}

names = ["industry", "services", "agriculture"]

pairs = [
    ["industry", "services"],
    ["industry", "agriculture"],
    ["services", "agriculture"]
]


def f_anova(groups, names):

    all_data = []

    for name in names:
        for x in groups[name]:
            all_data.append(x)

    total_mean = statistics.mean(all_data)

    ss_between = 0
    ss_within = 0

    for name in names:
        data = groups[name]

        mean = statistics.mean(data)

        ss_between += len(data) * (mean - total_mean)**2

        for x in data:
            ss_within += (x - mean)**2

    k = len(names)
    N = len(all_data)

    df_between = k - 1
    df_within = N - k

    ms_between = ss_between / df_between
    ms_within = ss_within / df_within

    F = ms_between / ms_within

    return F


F = f_anova(wages, names)

print("F =", F)

if F > 3.682:
    print("farz 0 rad mishavad")
else:
    print("farz 0 rad nemishavad")
