import board
from django.shortcuts import render, redirect
from board.models import Board
from member.models import Member

# Create your views here.


def list(request):
    bdlist = board.objects.values('id','title','userid','regdate','views').order_by('-id')

    context = {'bds': bdlist}
    return render(request, 'board/list.html', context)


def view(request):
    return render(request, 'board/view.html')


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
            board = Board(title=form['title'], contents=form['contents'], userid=Member.objects.get(pk=form['memberid']))
            board.save()    # Board 객체에 담은 게시글을 테이블에 저장

            return redirect('/list')

        context = {'form': form, 'error': error}

        return render(request, returnPage, context)