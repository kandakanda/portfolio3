from django.shortcuts import render, redirect
from students.models import Student, Course
from .models import Attendance
import datetime
from django.shortcuts import get_object_or_404
from decimal import Decimal
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def AttendanceSearchView(request):
    """
    出欠席の検索ビュー。

    学生の入学年度、クラス、日付を条件にフィルタを実行し、該当する学生リストを取得します。
    また、検索フォームに必要な情報（年度、月、クラス一覧）をコンテキストとして提供します。

    Args:
        request: HTTPリクエストオブジェクト（GETまたはPOST）

    Returns:
        HttpResponse: attendance_list.html テンプレートをレンダリングしたレスポンスを返します。

    コンテキスト:
        - course_all: 全てのクラスデータ（`Course` モデル）
        - ent_year: 選択可能な入学年度（現在の年を基準に過去10年から未来10年まで）
        - monthes: 1～12の月リスト
        - select_year: 検索された入学年度（POSTデータから取得）
        - select_day: 検索された日付（POSTデータから取得）
        - select_class: 検索されたクラスID（POSTデータから取得）
        - students: 検索条件に一致する学生リスト（`Student` モデル）

    Notes:
        - POSTリクエストがない場合はデフォルトで空の検索条件を保持します。
        - 年度選択の範囲は、現在の年を基準に過去10年から未来10年としています。

    Example:
        POSTデータの例:
        {
            'year': 2023,
            'class': 'C001',
            'day': '2023-12-05'
        }

        この場合、2023年度に入学したクラスIDがC001の学生が取得されます。

    """

    select_year = ''
    select_class = ''
    select_day = ''
    student_list = ''

    if request.POST:
        select_year = int(request.POST.get('year'))
        select_class = request.POST.get('class')
        select_day = request.POST.get('day')

        student_list = Student.objects.filter(ent_year=select_year, class_id=select_class).order_by('student_id')

    course_all = Course.objects.all().order_by('class_id')
    dt = datetime.datetime.today()  # ローカルな現在の日付と時刻を取得
    today_year = dt.year
    ent_year = []
    month = []
    for i in range(today_year-10, today_year+11):
        ent_year.append(i)

    for i in range(1, 13):
        month.append(i)

    context = {
        'course_all' : course_all,
        'ent_year' : ent_year,
        'monthes' : month,
        'select_year' : select_year,
        'select_day' : select_day,
        'select_class' : select_class,
        'students' : student_list,
    }
    return render(request, 'attendance/attendance_list.html', context)

@login_required
def AttendanceInsertView(request):
    """
    出欠席登録ビュー。

    フォームから送信されたPOSTデータを基に、学生の出欠情報をAttendanceモデルに登録し、
    学生の欠席累計データ（`absence_day`）を更新します。
    処理が終了した後、登録済みの学生データをテンプレートに渡します。

    Args:
        request: HTTPリクエストオブジェクト（POSTデータ必須）

    Returns:
        HttpResponse: 出欠席登録結果を表示する `attendance_insert_execute.html` をレンダリングして返します。
        または、POSTデータがない場合は出欠席検索画面にリダイレクトします。

    コンテキスト:
        - students: 更新対象となった `Student` インスタンスのリスト。
        - attendance_categories: 出欠席分類の辞書（キー：分類ID, 値：分類名）。
        - select_day: 選択された出欠日（POSTデータの `select_day`）。

    処理の流れ:
        1. POSTデータからキーと値を抽出し、学生IDと出欠席分類を取得します。
        2. `Attendance` モデルに新しい出欠データを登録します。
        3. 学生データ（`Student` モデル）の欠席累計（`absence_day`）を計算し、更新します。
        4. 更新後の学生データをテンプレートに渡して表示します。

    Notes:
        - 学生IDが無効な場合、`get_object_or_404` によって404エラーを返します。
        - `category = 0` の場合、出欠席データは登録されません。
        - 欠席累計は以下のルールで加算されます:
            - `1`: 欠席 -> `+1.0`
            - `2, 3`: 遅刻または早退 -> `+0.5`
            - その他: `+0.0`

    Example:
        POSTデータの例:
        {
            'select_day': '2024-12-05',
            'at_id_student_001': '1',
            'at_id_student_002': '3'
        }

        この場合、2024年12月5日の出欠データが以下のルールで登録されます:
        - 学生 001 -> 欠席 (分類1)
        - 学生 002 -> 早退 (分類3, 累計に0.5加算)
    """
    if request.POST:
        attendance_data = {}
        attendance_student = []
        select_day = request.POST.get('select_day')

        attendance_categories = {
        1: "欠席",
        2: "遅刻",
        3: "早退",
        4: "その他"
        }
        
        # POSTデータからキーを探索して収集
        for key, value in request.POST.items():
            if key.startswith("at_id_"):  # "at_id_" で始まる名前を探す
                student_id = key.split("_")[2]  # 学生IDを抽出
                attendance_data[student_id] = value

        for student_id, category in attendance_data.items():
            # 存在チェックと取得
            student = get_object_or_404(Student, student_id=student_id)
            if category != '0':
                Attendance.objects.create(
                    student_id=student,
                    attendance_id=category,
                    attendance_date=select_day
                )
            day = 0.0
            if category == '1':
                day += 1.0
            elif category in ['2', '3']:
                day += 0.5
            else:
                day += 0.0
            select_student = Student.objects.get(student_id=student_id)
            select_student.absence_day += Decimal(day)
            select_student.save()
            select_student = Student.objects.prefetch_related('attendance_set').get(student_id=student_id)
            attendance_student.append(select_student)

            # select_day = datetime.datetime.strptime(select_day, "%Y年%m月%d日").strftime("%Y-%m-%d")

        context = {
                'students' : attendance_student,
                'attendance_categories': attendance_categories,
                'select_day' : select_day,
            }
        return render(request, 'attendance/attendance_insert_execute.html', context)
    return redirect('attendance:at_search')