from django.shortcuts import render, redirect
import datetime
from django.views import generic
from students.models import Course, Student, Subject, Score
from .forms import SubjectForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def ScorelistView(request):
    """
    学生のスコアを表示およびフィルタリングするビュー関数。

    この関数は、選択された年度、クラス、科目に基づいて学生情報およびスコアをフィルタリングし、テンプレートにデータを渡します。

    引数:
        request: HttpRequestオブジェクト。

    戻り値:
        HttpResponse: フィルタリングされた学生のスコアデータを含むHTMLページ。

    コンテキストデータ:
        - course_all: すべてのコース情報 (class_id順)。
        - ent_year: 入学年度のリスト (現在の年 - 10年から現在の年 + 10年まで)。
        - subject_all: すべての科目情報 (subject_id順)。
        - select_year: POSTリクエストで選択された年度 (デフォルトは空)。
        - select_class: POSTリクエストで選択されたクラス (デフォルトは空)。
        - select_sub: POSTリクエストで選択された科目 (デフォルトは空)。
        - students: フィルタリングされた学生リスト (選択された年度とクラスに基づく)。
        - stu_subject: フィルタリングされたスコアリスト (選択された科目と学生リストに基づく)。
        - subject_dict: subject_idをキー、subject_nameを値とした辞書 (テンプレートでのクイックルックアップ用)。
    """
    select_year = ''
    select_class = '' 
    select_sub = ''
    student_list = ''
    stu_subject = ''
    subject_dict = {subject.subject_id: subject.subject_name for subject in Subject.objects.all()}
    if request.POST:
        select_year = int(request.POST.get('year'))
        select_class = request.POST.get('class')
        select_sub = request.POST.get('subject')

        student_list = Student.objects.filter(ent_year=select_year, class_id=select_class).order_by('student_id')
        stu_subject = Score.objects.filter(subject_id=select_sub, student_id__in=student_list)

    course_all = Course.objects.all().order_by('class_id')
    subject_all = Subject.objects.all().order_by('subject_id')
    dt = datetime.datetime.today()  # ローカルな現在の日付と時刻を取得
    today_year = dt.year
    ent_year = []
    for i in range(today_year-10, today_year+11):
        ent_year.append(i)

    context = {
        'course_all' : course_all,
        'ent_year' : ent_year,
        'subject_all' : subject_all,
        'select_year' : select_year,
        'select_sub' : select_sub,
        'select_class' : select_class,
        'students' : student_list,
        'stu_subject' : stu_subject,
        'subject_dict' : subject_dict,
    }
    return render(request, 'scores/score_list.html', context)

@login_required
def ScoreExecuteView(request):
    """
    生徒の点数を登録・更新するビュー

    このビューでは、POSTリクエストで送信されたフォームデータを基に、生徒の点数を登録または更新します。
    リクエスト内で送信された「select_class」「select_year」「select_sub」といったデータに基づき、
    対象のクラス、年度、科目に対して、生徒の点数が保存または更新されます。

    フォームで送られた学生IDごとのスコアデータ（「score_学生ID」）を利用し、既存の生徒に関連するスコアを更新し、
    必要があれば新たにスコアを登録します。

    成功した場合、メッセージを表示し、フォームを再描画します。

    Returns:
        render: 点数登録/更新画面を表示するテンプレートとコンテキストを返す。
        redirect: POSTリクエストがない場合はスコア一覧ページにリダイレクト。

    Args:
        request: HTTPリクエストオブジェクト。この中にPOSTデータ（フォームデータ）が含まれる。

    """
    scores_data = {}
    select_class = ''
    select_year = ''
    if request.POST:
        subject_dict = {subject.subject_id: subject.subject_name for subject in Subject.objects.all()}

        select_class = request.POST.get('select_class')
        select_year = request.POST.get('select_year')

        select_sub = request.POST.get('select_sub')
        for key, value in request.POST.items():
            if key.startswith("score_"):  # "score_" で始まる名前を探す
                student_id = key.split("_")[1]  # 学生IDを抽出
                scores_data[student_id] = value

        subject = get_object_or_404(Subject, subject_id=select_sub)
        for student_id, category in scores_data.items():
            # 存在チェックと取得
            student = get_object_or_404(Student, student_id=student_id)
            if category != '':
                Score.objects.update_or_create(
                student_id=student,
                subject_id=subject,
                defaults={'score': category}
                )
                messages.success(request, "点数を登録・更新しました。")

        students = Student.objects.filter(ent_year=select_year, class_id=select_class).order_by('student_id')
        context = {
             'students' : students,
             'select_sub' : select_sub,
             'subject_dict' : subject_dict,
        }
        return render(request, 'scores/score_execute.html', context) 
    
    return redirect('scores:score_list')

@login_required
def SubjectListView(request):
    """
    科目一覧を表示するビュー

    このビューでは、データベースから全ての科目を取得し、それを科目ID順に並べ替えて一覧として表示します。
    科目一覧はテンプレートである「subject_list.html」に渡され、ユーザーに表示されます。

    Returns:
        render: 科目一覧画面を表示するテンプレートとコンテキストを返す。

    Args:
        request: HTTPリクエストオブジェクト。このリクエストには特にデータは含まれていませんが、
                 ビューのレスポンスとして科目一覧を返すために使用されます。
    """
    sub_list = Subject.objects.all().order_by('subject_id')
    context = {
        'sub_list' : sub_list,
    }
    return render(request, 'scores/subject_list.html', context)

class SubjectCreateView(LoginRequiredMixin, generic.CreateView):
    """
    科目登録ビュー。

    新しい科目をデータベースに登録するためのフォームを表示し、登録処理を実行します。

    クラス属性:
        model (Model): 登録対象のモデル（`Subject`）。
        template_name (str): 使用するテンプレートファイル（`scores/subject_create.html`）。
        form_class (Form): フォームクラス（`SubjectCreateForm`）。
        success_url (str): 登録成功後のリダイレクト先URL（`scores:sub_list`）。

    メソッド:
        form_valid(self, form): フォームが有効な場合の追加処理を実装。
            - フォームから保存処理を実行。
            - 成功メッセージを表示。
            - 成功後のリダイレクトを実行。

    Notes:
        - 成功メッセージにはDjangoの`messages`フレームワークを使用しています。
        - 登録完了後は科目一覧ページ（`sub_list`）に遷移します。
    """
    model = Subject
    template_name = 'scores/subject_create.html'
    form_class = SubjectForm
    success_url = reverse_lazy('scores:sub_list')

    def form_valid(self, form):
        """
        フォームが有効な場合の処理。

        このメソッドは、フォームの検証が成功した場合に呼び出されます。
        フォームデータを保存し、ユーザーに成功メッセージを表示します。

        Parameters:
            form (django.forms.ModelForm): 検証に成功したフォームインスタンス。

        Returns:
            HttpResponseRedirect: 成功後にリダイレクトするレスポンス。
        """
        score = form.save(commit=False)
        score.save()
        messages.success(self.request, "科目を登録しました。")
        return redirect('scores:sub_list')

@login_required
def SubjectUpdateView(request, pk):
    """
    科目情報を更新するビュー。

    指定された `subject_id` の科目情報を編集し、POSTリクエストで変更を保存します。
    GETリクエスト時には現在の科目情報を表示し、編集フォームとして提供します。

    Parameters:
        request (HttpRequest): HTTPリクエストオブジェクト
        pk (str): 更新する科目の主キー（科目番号）

    Returns:
        HttpResponse: 更新ページ (`subject_update.html`) へのレンダリングレスポンス、
                      またはリダイレクトレスポンス (`scores:sub_list`)。
    """

    sub_pk_data = Subject.objects.get(subject_id=pk)
    form = SubjectForm(instance=sub_pk_data,)
    context = {
        'form' : form,
    }
    if request.POST.get('next', '') == 'update':
        form = SubjectForm(request.POST, instance=sub_pk_data)
        if form.is_valid():
            form.save()
            messages.success(request, "科目情報を変更しました。")
            return redirect('scores:sub_list')
        else:
            messages.success(request, "科目情報を変更できませんでした。")
            return render(request, 'scores/subject_update.html', context)
    return render(request, 'scores/subject_update.html', context)

class SubjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    """
    科目情報を削除するビュー。

    指定された `subject_id` の科目情報を削除します。
    削除後、科目一覧ページ（`scores:sub_list`）にリダイレクトします。

    Parameters:
        request (HttpRequest): HTTPリクエストオブジェクト。
        pk (str): 削除する科目の主キー（科目番号）。

    Returns:
        HttpResponse: 削除後、科目リストページ（`scores:sub_list`）にリダイレクトします。
    """
    model = Subject
    success_url = reverse_lazy('scores:sub_list')  # 科目一覧ページにリダイレクト
    template_name = 'scores/subject_confirm_delete.html'  # 削除確認ページのテンプレート

     # GET メソッドで削除確認ページを表示
    def get(self, request, *args, **kwargs):
        """
        GET メソッドによる科目削除確認ページの表示。

        指定された科目を削除する前に、ユーザーに削除確認を促します。
        削除対象の科目情報をテンプレートに渡して、確認ページを表示します。

        Parameters:
            request (HttpRequest): HTTPリクエストオブジェクト
            *args (tuple): 他の位置引数
            **kwargs (dict): URLパラメータに基づくキーワード引数。科目ID（`subject_id`）

        Returns:
            HttpResponse: 削除確認ページを表示するための `subject_confirm_delete.html` テンプレートのレンダリング結果
        """
        subject = self.get_object()
        context = {
            'subject': subject  # 削除対象の科目情報を表示
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        POST メソッドによる科目削除処理。

        ユーザーが削除確認ページで「削除」ボタンを押すと、該当の科目情報をデータベースから削除します。
        削除が成功した後、科目リストページにリダイレクトし、削除成功メッセージを表示します。

        Parameters:
            request (HttpRequest): HTTPリクエストオブジェクト
            *args (tuple): 他の位置引数
            **kwargs (dict): URLパラメータに基づくキーワード引数。科目ID（`subject_id`）

        Returns:
            HttpResponse: 削除後、科目一覧ページ（`scores:sub_list`）へリダイレクトします
        """
        subject = self.get_object()
        subject.delete()
        messages.success(request, f"科目 {subject.subject_name} を削除しました。")
        return redirect(self.success_url)    