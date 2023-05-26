import random
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.core.paginator import Paginator

from app.models import Transaction


def index(request) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("/account")
    else:
        return render(request, "index.html")


def account(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("/")

    search = request.GET.get("search", "")

    transactions = Transaction.objects.filter(user=user).order_by("-id")
    if search != "":
        transactions = transactions.filter(description__icontains=search)

    paginator = Paginator(transactions, 10)
    page: int = 1
    if request.GET.get("page"):
        page = int(request.GET.get("page"))

    page_object = paginator.get_page(page)
    transactions = page_object.object_list
    return render(request, 'account.html', {
        'user': user,
        'transactions': transactions,
        'number_of_pages': paginator.num_pages,
        'count_of_pages': paginator.page_range,
        'current_page': page,
        'has_next': page_object.has_next(),
        'has_previous': page_object.has_previous(),
        'next_page': page + 1,
        'previous_page': page - 1,
        'search': search,
    })


def create_views(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        if request.POST.get("type", "") == "expense":
            Transaction.objects.create(
                user=user,
                description=request.POST.get("description", ""),
                amount=-abs(int(request.POST.get("amount", 0))),
            )
        if request.POST.get("type", "") == "income":
            Transaction.objects.create(
                user=user,
                description=request.POST.get("description", ""),
                amount=abs(int(request.POST.get("amount", 0)))
            )
        return redirect("/")

    raise NotImplementedError


def delete_views(request: HttpRequest, transaction_id: int) -> HttpResponse:
    Transaction.objects.filter(id=transaction_id).filter(user=request.user).delete()
    return redirect("/")


def edit_views(request: HttpRequest, transaction_id: int) -> HttpResponse:
    transaction = Transaction.objects.filter(id=transaction_id).filter(user=request.user).first()

    if request.method == "POST":
        transaction.description = request.POST.get("description", "")
        if request.POST.get("type", "") == "expense":
            transaction.amount = -abs(int(request.POST.get("amount", 0)))
        if request.POST.get("type", "") == "income":
            transaction.amount = abs(int(request.POST.get("amount", 0)))
        transaction.save()
        return redirect("/")

    return NotImplementedError


def add10(request:HttpRequest) -> HttpResponse:
    user = request.user
    if not user.is_authenticated:
        return redirect("/")

    description_expenses = [
        "Buying vegetables",
        "Buying household goods",
        "Buying iphone",
        "Buying TV",
        "Buying travel card",
        "Bought a new fridge",
        "Bought a new microwave",
        "Bought a new toaster",
    ]

    description_income = [
        "Salary",
        "Scholarship",
        "Business",
        "Got a bonus",
        "Got a gift",
        "Got a lottery",
    ]
    for i in range(10):
        Transaction.objects.create(

            user=user,
            description=random.choice(description_expenses),
            amount=-abs(random.randint(200, 1000)),
        )
    for i in range(5):
        Transaction.objects.create(
            user=user,
            description=random.choice(description_income),
            amount=abs(random.randint(1000, 5000))
        )
    return redirect("/")
