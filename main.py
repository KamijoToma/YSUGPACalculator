import csv
import argparse

# 绩点映射表
score_to_gpa = [
    (97, 100, 'A+', 4.5),
    (93, 96, 'A', 4.3),
    (89, 92, 'A-', 4.0),
    (85, 88, 'B+', 3.8),
    (81, 84, 'B', 3.4),
    (77, 80, 'B-', 3.0),
    (73, 76, 'C+', 2.6),
    (69, 72, 'C', 2.2),
    (65, 68, 'C-', 1.8),
    (60, 64, 'D', 1.2),
    (40, 59, 'F', 0),
    (0, 39, 'F-', 0),
]

def get_gpa_from_score(score, level):
    """根据百分制或等级制成绩返回绩点"""
    if level:
        for _, _, lvl, gpa in score_to_gpa:
            if level == lvl:
                return gpa
    try:
        score = float(score)
        for low, high, _, gpa in score_to_gpa:
            if low <= score <= high:
                return gpa
    except:
        pass
    return 0

def calculate_gpa(filename):
    # 自动检测编码
    encodings = ['utf-8-sig', 'gbk']
    for enc in encodings:
        try:
            with open(filename, encoding=enc) as f:
                # 尝试读取一行，判断能否解码
                f.readline()
            encoding = enc
            break
        except Exception:
            continue
    else:
        print('无法识别文件编码，请确认文件为UTF-8或GBK编码')
        return
    with open(filename, encoding=encoding) as f:
        reader = csv.DictReader(f)
        total = 0.0
        total_credits = 0.0
        for row in reader:
            # 只统计主修培养方案内课程的正考成绩
            if row['是否主修'] != '是' or row['考试类型'] not in ('', '考试', '考查') or row['重修重考'] != '正考':
                continue
            if row['是否有效'] != '是' or row['是否及格'] != '是':
                continue
            try:
                credit = float(row['学分'])
            except:
                continue
            is_degree = row['是否学位课'] == '是'
            try:
                gpa = float(row['绩点'])
            except:
                gpa = get_gpa_from_score(row['百分制成绩'], row['总成绩'])
            if is_degree:
                total += gpa * credit * 1.2
                total_credits += credit * 1.2
            else:
                total += gpa * credit
                total_credits += credit
        if total_credits == 0:
            print('无有效课程，无法计算GPA')
        else:
            print(f'加权平均学分绩点（GPA）：{total / total_credits:.4f}')

def main():
    parser = argparse.ArgumentParser(
        description='YSU GPA 计算器：根据教务导出的csv文件，自动计算加权平均学分绩点。\n'
                    '只统计主修培养方案内课程的正考成绩，学位课学分和绩点按1.2倍计入。',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('-f', '--file', required=True, help='CSV成绩文件路径，必须指定')
    args = parser.parse_args()
    calculate_gpa(args.file)

if __name__ == '__main__':
    main()
