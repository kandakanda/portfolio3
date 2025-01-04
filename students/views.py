from django.views import generic
from .models import Student, Course
from django.shortcuts import redirect, render
from .forms import StudentCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.urls import reverse

# Create your views here.
class HomeView(generic.TemplateView):
    template_name = "students/home.html"

class IndexView(LoginRequiredMixin, generic.TemplateView):
    """
    トップページを表示するためのクラスベースビュー。
    `index.html` を使用して、トップページを表示します。

    引数:
        request (HttpRequest): HTTPリクエストオブジェクト
        *args, **kwargs: URL から渡される任意の引数
    戻り値:
        TemplateResponse: 'index.html' テンプレートを使用して生成されたレスポンス
    使用例:
        IndexView.as_view()(request)
    """
    template_name = 'students/index.html'

@login_required
def student_listView(request):
    """
    学生一覧を表示するビュー

    引数:
        request (HttpRequest): HTTPリクエストオブジェクト
    戻り値:
        render: 表示する学生一覧情報をstudents_list.htmlへ送る
    使用例:
        student_listView(request)
    """
    students = Student.objects.all().filter(attend_flag=True).order_by('student_id')
    context = {'students': students,}
    return render(request, 'students/students_list.html', context)


class StudentCreateView(LoginRequiredMixin, generic.CreateView):
    """
    新しい学生情報をデータベースに登録するためのビュー。

    このビューは、新しい学生のレコードをフォームを使用して作成します。
    学生IDは、既存の学生IDの中で最も高い値を基にして、1を加算し、10桁の形式で学生IDを生成します。
    学生情報が正常に保存された後、成功ページにリダイレクトし、成功メッセージが表示されます。

    属性:
        model: 使用するモデル (Studentモデル)。
        template_name: フォームをレンダリングするためのテンプレート ('students_create.html')。
        form_class: 使用するフォームクラス (StudentCreateForm)。
        success_url: フォームが正常に送信された後にリダイレクトされるURL (reverse_lazy を使用して設定)。
    メソッド:
        form_valid(form):
            フォームが有効な場合にフォームの送信を処理します。新しい学生IDを生成し、
            フォームを保存後に成功メッセージを表示してリダイレクトします。
    """
    model = Student
    template_name = 'students/students_create.html'
    form_class = StudentCreateForm
    success_url = reverse_lazy('students:stu_create')

    def get_form_kwargs(self):
        """フォームにカスタム引数を渡す"""
        kwargs = super().get_form_kwargs()
        kwargs['is_create'] = True  # 新規作成フラグを渡す
        return kwargs

    def form_valid(self, form):
        """
        フォームが有効な場合に呼び出されるメソッド。

        このメソッドは、フォームの送信が成功した場合に呼ばれます。
        最新の学生IDを取得し、それに1を加算して新しい学生IDを生成します。
        この新しいIDを使用して学生を保存します。

        引数:
            form: ユーザーが入力したデータで検証されたフォーム。
        戻り値:
            redirect: フォームが有効な場合、成功メッセージを表示して、成功ページにリダイレクトします。
        """
        context = {
            'form': form,
        }
        if self.request.POST.get('next', '') == 'create':
            stu_id = ''
            latest_stu = Student.objects.order_by('-student_id').only('student_id').first()
            if latest_stu is None or latest_stu.student_id is None:
                stu_id = '0000000001'
            else:
                int_stu_id = int(latest_stu.student_id) + 1
                str_stu_id = str(int_stu_id).zfill(10)
                stu_id = str_stu_id
            student = form.save(commit=False)
            student.student_id = stu_id
            student.save()
            messages.success(self.request, "学生情報を登録しました。")
            return redirect('students:stu_create')

@login_required
def StudentDetailView(request):
    student_pk = ''
    if request.GET:
        student_pk = request.GET.get('student_pk')
    elif request.POST:
        student_pk = request.POST.get('student_pk')
    student_data = Student.objects.filter(student_id=student_pk).first()
    context = {
        'stu_data': student_data,
    }
    return render(request, 'students/student_detail.html', context)

@login_required
def StudentUpdateView(request):
    student_pk = ''
    if request.GET:
        student_pk = request.GET.get('student_pk')
    elif request.POST:
        student_pk = request.POST.get('student_pk')
    ago = request.POST.get('ago')
    student_data = Student.objects.filter(student_id=student_pk).first()

    if request.POST.get('next', '') == 'update_page':
        form = StudentCreateForm(instance=student_data, is_create=False)
        context={'form' : form,
                 'stu_data' : student_data,
                 'ago' : ago,
                 }

        return render(request, 'students/student_update.html', context)

    else:
        form = StudentCreateForm(request.POST)
        if form.is_valid():
            attend_flg  = request.POST.get('attend_flg')
            stu = Student.objects.get(student_id=student_pk)
            stu_updatedata = form.save(commit=False)
            stu_updatedata.student_id = student_pk
            stu_updatedata.absence_day = stu.absence_day
            # stu_updatedata.attend_flag = attend_flg
            # print(f'更新されたデータ: {stu_updatedata.attend_flag}')
            stu_updatedata.save()
            messages.success(request, "学生情報を変更しました。")
            if ago == 'list':
                return redirect("students:stu_list")
            else:
                return redirect(f'{reverse("students:stu_detail")}?student_pk={student_pk}')
        else:
            context={'form' : form,
                     'stu_data' : student_data,}
            messages.success(request, "学生情報を変更できませんでした。")
            return redirect('students:stu_update')

        


