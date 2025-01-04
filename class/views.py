from django.shortcuts import render, redirect
from django.views import generic
from students.models import Course
from accounts.models import Teacher
from .forms import ClassCreateForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def ClassListView(request):
    """
    クラスの一覧を表示するビュー関数。

    このビュー関数は、すべての `Course` インスタンス（クラス情報）を取得し、それらを `class_id` の順で並べ替えて表示します。
    また、`Teacher` モデルから全ての教師情報を取得し、教師IDをキーとして教師名を値とする辞書を作成し、テンプレートに渡します。

    処理内容:
    1. 全ての `Course` インスタンスを取得し、`class_id` 順で並べ替える。
    2. 全ての `Teacher` インスタンスから、教師IDと教師名のペアを辞書にして取得する。
    3. `classes`（クラス情報）と `teacher`（教師情報）をコンテキストとして `class_list.html` テンプレートに渡す。

    引数:
    - request (HttpRequest): HTTPリクエストオブジェクト。

    戻り値:
    - HttpResponse: `class_list.html` テンプレートがレンダリングされ、`classes` と `teacher` を含んだコンテキストが返されます。
    """
    # クラス情報を class_id の順で取得
    classes = Course.objects.all().order_by('class_id')
    # 教師IDと教師名を辞書形式で取得
    teacher = {teacher.teacher_id: teacher.teacher_name for teacher in Teacher.objects.all()}
    
    # テンプレートに渡すコンテキスト
    context = {
        'classes': classes,
        'teacher': teacher,
    }

    # テンプレートをレンダリングしてレスポンスを返す
    return render(request, 'class/class_list.html', context)


class ClassCreateView(LoginRequiredMixin, generic.CreateView):
    """
    クラス情報を新規作成するためのビュークラス。

    このビュークラスは、`Course` モデルを使用してクラス情報を新規作成します。クラス登録フォームは、`ClassCreateForm` を使用して表示され、フォームが有効な場合には新しい `Course` インスタンスがデータベースに保存されます。
    フォームが正常に送信された場合、ユーザーには登録完了メッセージが表示され、クラス一覧ページへリダイレクトされます。

    処理内容:
    1. `get_context_data` メソッドで、テンプレート用のコンテキストを追加。
    2. フォームが有効な場合、`form_valid` メソッドでフォームの内容を保存し、成功メッセージを表示。
    3. フォーム送信後、クラス一覧ページ（`cls_list`）へリダイレクト。

    引数:
    - request (HttpRequest): HTTPリクエストオブジェクト。

    戻り値:
    - HttpResponse: 新しいクラス情報のフォームを表示するための `class_create.html` テンプレートをレンダリングします。また、フォームが正常に送信された場合は、登録完了メッセージと共にクラス一覧ページにリダイレクトされます。

    例外:
    - form_invalid: フォームの内容が不正な場合は、エラーメッセージを表示します。
    """

    model = Course  # ここでモデルが正しく設定されていること
    template_name = 'class/class_create.html'
    form_class = ClassCreateForm
    success_url = reverse_lazy('class:cls_list')


    # クラス作成用のフォームを表示する際に追加するコンテキスト
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'クラス情報登録'  # テンプレートでタイトルを表示
        return context

    # フォームが有効であれば、データベースに新規作成してリダイレクト
    def form_valid(self, form):
        form.save()  # クラス情報をデータベースに保存
        messages.success(self.request, "クラスを登録しました。")  # 成功メッセージを表示
        return redirect('class:cls_list')  # クラス一覧ページへリダイレクト


class ClassUpdateView(LoginRequiredMixin, generic.UpdateView):
    """
    既存のクラス情報を更新するためのビュークラス。

    このビュークラスは、`Course` モデルを使用して既存のクラス情報を更新します。クラス情報の編集フォームは、`ClassCreateForm` を使用して表示され、フォームが有効な場合には既存の `Course` インスタンスが更新されます。
    フォームが正常に送信された場合、ユーザーには更新完了メッセージが表示され、クラス一覧ページへリダイレクトされます。

    処理内容:
    1. `get_context_data` メソッドで、テンプレート用のコンテキストにタイトルを追加。
    2. フォームが有効な場合、`form_valid` メソッドでフォームの内容を保存（更新）し、成功メッセージを表示。
    3. フォーム送信後、クラス一覧ページ（`cls_list`）へリダイレクト。

    引数:
    - request (HttpRequest): HTTPリクエストオブジェクト。

    戻り値:
    - HttpResponse: クラス情報更新用のフォームを表示するための `class_create.html` テンプレートをレンダリングします。また、フォームが正常に送信された場合は、更新完了メッセージと共にクラス一覧ページにリダイレクトされます。

    例外:
    - form_invalid: フォームの内容が不正な場合は、エラーメッセージを表示します。
    """

    model = Course  # ここでモデルが正しく設定されていること
    template_name = 'class/class_create.html'
    form_class = ClassCreateForm
    success_url = reverse_lazy('class:cls_list')

    # クラス更新用のフォームを表示する際に追加するコンテキスト
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'クラス情報変更'  # テンプレートでタイトルを表示
        return context

    # フォームが有効であれば、データベースのクラス情報を更新しリダイレクト
    def form_valid(self, form):
        form.save()  # クラス情報をデータベースで更新
        messages.success(self.request, "クラスを更新しました。")  # 成功メッセージを表示
        return redirect('class:cls_list')  # クラス一覧ページへリダイレクト

class ClassDeleteView(LoginRequiredMixin, generic.DeleteView):
    """
    クラス情報を削除するためのビュークラス。

    このビュークラスは、指定された `Course` モデルのインスタンスを削除します。削除確認のため、`class_confirm_delete.html` テンプレートを使用してユーザーに削除確認を行わせます。削除が成功した場合、削除完了メッセージを表示し、指定された `cls_list` ページにリダイレクトされます。

    処理内容:
    1. `get` メソッドで削除対象のクラス情報を表示する確認ページを表示。
    2. `post` メソッドで実際に削除処理を行い、削除後に成功メッセージを表示してリダイレクト。

    引数:
    - request (HttpRequest): HTTPリクエストオブジェクト。
    - *args, **kwargs: URLパラメータから取得されるオプションの引数。

    戻り値:
    - HttpResponse: クラス削除確認用のフォームを表示する `class_confirm_delete.html` テンプレート、または削除後にクラス一覧ページ（`cls_list`）へリダイレクト。

    例外:
    - もし対象のクラス情報が存在しない場合、`get_object()` で取得できないことがあり得ます。
    """

    model = Course  # ここでモデルが正しく設定されていること
    template_name = 'class/class_confirm_delete.html'
    success_url = reverse_lazy('class:cls_list')

    # GETメソッドで削除確認ページを表示
    def get(self, request, *args, **kwargs):
        classes = self.get_object()  # 削除対象のクラスを取得
        context = {
            'classes': classes  # 削除対象の科目情報をテンプレートに渡す
        }
        return render(request, self.template_name, context)  # 確認ページをレンダリング

    # POSTメソッドで実際に削除処理を行う
    def post(self, request, *args, **kwargs):
        classes = self.get_object()  # 削除対象のクラスを取得
        classes.delete()  # クラス情報を削除
        messages.success(request, f"クラス {classes.course_name} を削除しました。")  # 削除メッセージを表示
        return redirect(self.success_url)  # 成功した場合、クラス一覧ページにリダイレクト