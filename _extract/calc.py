# -*- coding: utf-8 -*-
"""第一单元 实测数据 → 平均值 / 验收极限 / 合格性判定 计算与校核"""
import json

def stat(vals):
    n = len(vals)
    avg = sum(vals) / n
    return dict(n=n, avg=avg, rmax=max(vals), rmin=min(vals), R=max(vals) - min(vals))

def limits(nominal, up_dev, lo_dev, A, inset=True):
    U = nominal + up_dev          # 上极限尺寸
    L = nominal + lo_dev          # 下极限尺寸
    if inset:
        return U, L, round(U - A, 4), round(L + A, 4)
    return U, L, U, L

def verdict(avg, acc_hi, acc_lo):
    if avg > acc_hi:
        return '不合格（超上验收极限 %.4f）' % (avg - acc_hi)
    if avg < acc_lo:
        return '不合格（超下验收极限 %.4f）' % (acc_lo - avg)
    return '合格'

rows = []

def add(tag, part, feat, inst, nominal, desig, up_dev, lo_dev, A, vals, inset=True, note=''):
    s = stat(vals)
    U, L, AH, AL = limits(nominal, up_dev, lo_dev, A, inset)
    rows.append(dict(tag=tag, part=part, feat=feat, inst=inst, nominal=nominal, desig=desig,
                     up_dev=up_dev, lo_dev=lo_dev, A=A,
                     vals=vals, n=s['n'], avg=round(s['avg'], 4), R=round(s['R'], 4),
                     U=round(U, 4), L=round(L, 4), acc_hi=AH, acc_lo=AL,
                     verdict=verdict(s['avg'], AH, AL), note=note,
                     single_out=[v for v in vals if v > AH or v < AL]))

# ---- 表 4-1 ----
add('表4-1', '图4-7零件', '外圆 Φ15g7', '游标卡尺', 15, 'g7', -0.006, -0.024, 0.0018,
    [14.96, 14.98, 14.96, 15.04, 14.96])
add('表4-1', '图4-7零件', '外圆 Φ15g7', '外径千分尺', 15, 'g7', -0.006, -0.024, 0.0018,
    [14.970, 14.968, 14.967, 14.975, 14.990])

# ---- 项目一 上端盖 ----
add('项目一', '上端盖', '端盖安装外圆 φ68', '游标卡尺', 68, 'h6', 0.000, -0.019, 0.0019, [67.96, 67.86, 67.88])
add('项目一', '上端盖', '轴承安装孔 φ40', '游标卡尺', 40, 'H7', 0.025, 0.000, 0.0025, [39.86, 39.92, 39.98])
add('项目一', '上端盖', '密封圈孔 φ30', '游标卡尺', 30, 'H8', 0.033, 0.000, 0.0033, [29.98, 29.98, 30.02])

# ---- 项目二 下端盖 ----
add('项目二', '下端盖', '端盖安装外圆 φ35', '游标卡尺', 35, 'h6', 0.000, -0.016, 0.0016, [34.94, 34.86, 34.90])

# ---- 项目三 箱体 ----
add('项目三', '箱体', '长度 94', '游标卡尺', 94, '未注公差 m 级', 0.300, -0.300, 0.0, [93.54, 93.60, 93.64], inset=False)
add('项目三', '箱体', '长度 54', '游标卡尺', 54, '未注公差 m 级', 0.300, -0.300, 0.0, [54.00, 53.96, 53.98], inset=False)
add('项目三', '箱体', '内孔 φ68', '游标卡尺', 68, 'H7', 0.030, 0.000, 0.0030, [67.98, 68.00, 67.98])
add('项目三', '箱体', '内孔 φ35', '内径表', 35, 'H7', 0.025, 0.000, 0.0025, [34.939, 34.945, 34.950])

# ---- 项目四 蜗轮轴 ----
add('项目四', '蜗轮轴', '轴颈 φ17（左）', '外径千分尺', 17, 'k6', 0.012, 0.001, 0.0011, [17.005, 16.964, 16.996])
add('项目四', '蜗轮轴', '轴颈 φ20（中）', '外径千分尺', 20, 'k6', 0.015, 0.002, 0.0013, [19.990, 20.015, 20.033])
add('项目四', '蜗轮轴', '轴颈 φ17（右）', '外径千分尺', 17, 'k6', 0.012, 0.001, 0.0011, [17.010, 16.961, 16.974])

# ---- 项目五 量规（判定对象：量规本身的极限尺寸，不走 A 内缩） ----
add('项目五', '孔用工作量规', '通规（φ35H7 用）', '外径千分尺', 35, '量规 35(+0.0055/+0.0025)', 0.0055, 0.0025, 0.0, [34.989, 34.987], inset=False)
add('项目五', '孔用工作量规', '止规（φ35H7 用）', '外径千分尺', 35, '量规 35(+0.025/+0.022)', 0.025, 0.022, 0.0, [35.002, 35.005], inset=False)

out = []
for r in rows:
    out.append('%-5s %-8s %-16s %-10s n=%d 均值=%.4f R=%.4f | 极限 %s~%s | 验收 %s~%s | %s'
               % (r['tag'], r['part'], r['feat'], r['inst'], r['n'], r['avg'], r['R'],
                  r['L'], r['U'], r['acc_lo'], r['acc_hi'], r['verdict']))
    if r['single_out']:
        out.append('        单次越验收极限的值: %s' % r['single_out'])
    if r['R'] > (r['U'] - r['L']):
        out.append('        [!] 分散量 %.4f 已大于公差带宽 %.4f' % (r['R'], r['U'] - r['L']))

ok = [r for r in rows if r['verdict'] == '合格']
out.append('')
out.append('合格 %d 项 / 共 %d 项' % (len(ok), len(rows)))
for r in ok:
    out.append('  合格: %s %s 均值=%s' % (r['tag'], r['feat'], r['avg']))

with open(r'C:\Users\Admin\Desktop\公差配合实训\_extract\_calc_report.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
with open(r'C:\Users\Admin\Desktop\公差配合实训\公差配合实训资料包\_calc.json', 'w', encoding='utf-8') as f:
    json.dump(rows, f, ensure_ascii=False, indent=1)
print('done')
