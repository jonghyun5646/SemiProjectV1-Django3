from django.db.models import F
from django.views.decorators.cache import cache_control
from django.shortcuts import render, redirect
from board.models import Board
from member.models import Member

# Create your views here.


def list(request):
    # select 'id','title','userid','regdate','views' from board order by id desc
    # bdlist = board.objects.values('id','title','userid','regdate','views').order_by('-id')

    # Board와 Member 테이블은 userid <-> id 컬럼을 기준으로 inner join을 수행
    bdlist = Board.objects.select_related('member')

    # join된 member 테이블의 userid 확인
    # bdlist.get(0).member.userid

    context = {'bds': bdlist}
    return render(request, 'board/list.html', context)

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def view(request):
    if request.method == 'GET':
        form = request.GET.dict()
        # print(form['bno'])

        # 본문글에 대한 조회수 증가
        # update board set views = views + 1 where id = ??
        # b = Board.objects.get(id=form['bno'])
        # b.views = b.views + 1
        # b.save()
        Board.objects.filter(id=form['bno']).update(views=F('views') + 1)

        # 본문글 조회
        # select * from board inner join member using(id) where id = ??
        bd = Board.objects.select_related('member').get(id=form['bno'])

    elif request.method == 'POST':
        pass

    context = {'bd': bd}
    return render(request, 'board/view.html', context)


def write(request):
    returnPage = 'board/write.html'
    form = ''
    error = ''

    if request.POST == 'GET':
        return render(request, returnPage)

    elif request.POST == 'POST':
        form = request.POST.dict()

        # 유효성 검사
        if not (form['title'] and form['contents']):
            error = '제목이나 본문을 작성하세요!'
        else:
            # 입력한 게시글을 Board 객체에 담음
            board = Board(title=form['title'], contents=form['contents'], member=Member.objects.get(pk=form['memberid']))
            board.save()    # Board 객체에 담은 게시글을 테이블에 저장

            return redirect('/list')

        context = {'form': form, 'error': error}

        return render(request, returnPage, context)


def remove(request):
    if request.method == 'GET':
        form = request.GET.dict()

        # delete from board where bno = ??
        Board.objects.filter(id=form['bno']).delete()

    return redirect('/list')


def modify(request):
    bd = None
    if request.method == 'GET':
        form = request.GET.dict()

        # select * from board where bno = ??
        bd = Board.objects.get(id=form['bno'])

    elif request.method == 'POST':
        form = request.POST.dict()

        # update board set title = ??, contents = ?? where bno = ??
        # b = Board.objects.get(id=form['bno'])
        # b.title = form['title']
        # b.contents = form['contents']
        # b.save()

        Board.objects.filter(id=form['bno']).update(title=form['title'], contents=form['contents'])

        # 본문글 수정완료시 view 페이지로 이동
        return redirect('/view?bno=' + form['bno'])

    context = {'bd': bd}
    return render(request, 'board/modify.html', context)