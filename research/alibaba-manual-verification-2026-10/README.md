# KIKFIA: live Alibaba factory verification (prepared 5 Oct 2026)

## Status: the live Alibaba inspection has NOT been done yet

You asked for manual research on Alibaba in your own browser: open each store, read the verification panel, read the 1–3★ reviews, and confirm every link. **The session that prepared this folder could not do that, and it did not pretend to.**

| Blocker | Detail |
|---|---|
| No access to your PC | This session ran in a Claude Code **cloud container**. It cannot see or control the Alibaba tab open on your computer. No browser-control or computer-use tool was connected. |
| Alibaba blocked | The cloud environment's network policy rejected `alibaba.com`, `www.alibaba.com` and `*.en.alibaba.com` (tested with direct requests and the web-fetch tool). |

The earlier report in [`../alibaba-direct-factories-2026-10/REPORT.md`](../alibaba-direct-factories-2026-10/REPORT.md) was built from **search-engine copies** of Alibaba pages. It is **not** the manual verification you asked for. Use it only as a starting list.

## How to unblock (pick one)

1. **Recommended: run the research on your own computer.** Open the **Claude desktop app** and turn on **Claude in Chrome** (the browser extension) or computer use. Claude can then drive the Alibaba tab you already have open and are logged into. Being logged in matters, because Alibaba hides some supplier details and contact options from logged-out visitors. Paste the hand-off prompt below.
2. **Do the clicks yourself.** Follow the click path on the workbook's *Read Me* sheet and type what you see into the yellow cells. Scores, priorities, the Master Table and the Top 10 fill themselves in.
3. **Allow Alibaba in this cloud environment.** In the session's cloud-environment menu, choose **Edit → Network access**, then either pick a broader level or choose *Custom* and add `alibaba.com` and `*.alibaba.com` under Allowed domains, keeping the default package-manager list (steps: <https://code.claude.com/docs/en/cloud-environments#network-access>). **Caveat:** Alibaba often shows slider CAPTCHAs to data-centre traffic, and a cloud browser is not logged in as you. Expect this to be partly or fully blocked even after the change. Option 1 is more reliable.

### Hand-off prompt (paste into a Claude desktop session with Claude in Chrome enabled)

> Open `research/alibaba-manual-verification-2026-10/kikfia-alibaba-factory-verification.xlsx` from the KIKFIA repo (branch `claude/sweet-dirac-wfyi47`) and follow its *Read Me* sheet. Use Claude in Chrome on my already-open, logged-in Alibaba tab. Run the keywords on the *Search Log* sheet. For every candidate, follow click path a–i: open the store, inspect Company Profile, Verification/Assessment, Factory/Production, Reviews (filter to 1★, 2★ and 3★ and read them), two product pages and the official website. Fill every yellow cell with exactly what Alibaba shows. Write NOT CLEAR / NOT SHOWN instead of guessing. Score each company on the *Scoring* sheet. Stop at 30 genuine A/B factories, or report the real number if fewer qualify. Then write the company-by-company report (20 fields each), the Top 10 and the master table from the workbook.

## What's in the workbook

`kikfia-alibaba-factory-verification.xlsx` has 7 sheets.

| Sheet | What it does |
|---|---|
| **Read Me** | Status warning, legend, the 9-step click path for each company, gates and scoring rules. |
| **Inspection Log** | One row per company (60 rows), with 54 columns covering all 20 report fields and every check you listed. Row 2 is a fictional example that shows the format. Rows 1–27 are pre-loaded only with names, store URLs and the *prior unverified* concerns to re-check. The verification columns are blank. |
| **Scoring** | Your 100-point model (25/20/15/10/10/10/5/5) with input limits. Calculates the total, the factory/customization gate, a suggested priority, your override, the final priority and a rank. |
| **Master Table** | Your exact 15 columns, filled automatically, with clickable store, product and website links. |
| **Top 10** | The 10 highest-ranked A/B companies, filled automatically with the fields you asked for. |
| **Search Log** | 52 Alibaba keywords across every category you listed (plus ADU, granny-flat, glamping-pod, SIP and US-standard terms), with columns to record filters, pages reviewed and candidates found. |
| **Previously Rejected** | 21 companies dropped earlier for trader signals or weak evidence. Re-inspect one only if the live store contradicts the reason. |

### Rules built into the formulas

- **Hard gates:** a company is automatically **C** unless *Factory or Trading?* = `FACTORY` **and** *Full customization?* = `YES`. This enforces your "full customization is mandatory" and "factories only" rules.
- **Suggested priority:** A at 80 or above, B at 60 or above, otherwise C. *These thresholds are my suggestion, because you defined A/B/C in words only. Change them in Scoring!B2:B3.* Your override column always wins.
- **Ranking:** only A and B companies are ranked. A tie goes to the lower row number.
- Only 10 rows feed the Top 10. The Master Table lists every row, so filter its Priority column to A and B for the final list.

## Starting queue (store links NOT yet opened live)

These 27 come from the earlier search-indexed research. They are a queue to inspect, **not** a verified list. You need about 30 genuine A/B factories. Expect to inspect 50–60 companies, so new ones from the live keyword searches go into rows 28–60.

| # | Company | Store |
|---|---|---|
| 1 | Beijing Chengdong International Modular Housing Corporation (CDPH) | https://cdph.en.alibaba.com/ |
| 2 | Ningbo Deepblue Smarthouse Co., Ltd. | https://deepblue.en.alibaba.com/ |
| 3 | Hebei Weizhengheng Modular House Technology Co., Ltd. (WZH) | https://wzhhouse.en.alibaba.com/ |
| 4 | Zhejiang Putian Integrated Housing Co., Ltd. (PTH) | https://putiangroup.en.alibaba.com/ |
| 5 | Zhuhai Remac Space Co., Ltd. | https://remacspace.en.alibaba.com/ |
| 6 | Guangdong Zhonghuilvjian Moving House Technology Co., Ltd. (CGCH) | https://cgcontainer.en.alibaba.com/ |
| 7 | Shandong Mars Cabin Technology Co., Ltd. | https://marscastle.en.alibaba.com/ |
| 8 | Guangzhou Moneybox Steel Structure Engineering Co., Ltd. | https://moneyboxcontainer.en.alibaba.com/ |
| 9 | Foshan The Box Modular House Co., Ltd | https://thebox.en.alibaba.com/ |
| 10 | Fucheng Huaying Integrated Housing Co., Ltd. | https://fchuaying.en.alibaba.com/ |
| 11 | Hebei Shengyuan Tongda Modular House Co., Ltd. | https://shengyuantongda.en.alibaba.com/ |
| 12 | Heshi (Hebei) Integrated Housing Co., Ltd. | https://heshihouse.en.alibaba.com/ |
| 13 | Suzhou Zhongnan Steel Structure Co., Ltd. | https://sz-zhongnan.en.alibaba.com/ |
| 14 | Foshan Hege Steel Modular Housing Co., Ltd. | https://hege-prefabhouse.en.alibaba.com/ |
| 15 | Weifang Henglida Steel Structure Co., Ltd. (Lida Group) | https://prefab-house.en.alibaba.com/ |
| 16 | Dongguan Toppre Modular House Co., Ltd. | https://topprehouse.en.alibaba.com/ |
| 17 | Tianjin Yuantai Module House Co., Ltd. | https://zhongguoyuantai.en.alibaba.com/ |
| 18 | Weifang Ante Steel Structure Engineering Co., Ltd. | https://antehouse.en.alibaba.com/ |
| 19 | Hebei Baida Mingsheng Integrated Housing Co., Ltd. | https://baidamingsheng.en.alibaba.com/ |
| 20 | Laizhou Dingrong Steel Structure Co., Ltd. | https://prefabbuilding.en.alibaba.com/ |
| 21 | Hebei Zhongxinhe Assembled Housing Manufacturing Co., Ltd. | https://hbzxh.en.alibaba.com/ |
| 22 | Guangdong Cbox Co., Limited | https://cbox.en.alibaba.com/ |
| 23 | Dalian Xiesheng Construction Industry Co., Ltd. | https://xsbuild.en.alibaba.com/ |
| 24 | Linyi Jianjie Exhibition Tent House Co., Ltd. (Runtai) | https://runtaicabin.en.alibaba.com/ |
| 25 | Foshan Yinneng Green Construction Technology Co., Ltd. | https://yinnenggreen.en.alibaba.com/ |
| 26 | Suzhou Daxiang Container House Co., Ltd. | https://dxhcontainer.en.alibaba.com/ |
| 27 | Orient GS International Engineering Co., Ltd. (GS Housing) | https://gshousing.en.alibaba.com/ |
