from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Sum, Case, When, DecimalField, F

from .models import Transaction, Category, Emotion
from .forms import CustomUserCreationForm
from .models import Transaction, Category, Emotion, Goal
from decimal import Decimal, InvalidOperation
from .models import Goal, Transaction, Category, Emotion

from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from datetime import datetime

from collections import defaultdict
from django.db.models import Sum
from django.db.models.functions import Coalesce
import json
from django.db.models import Sum, F
from django.db.models.functions import TruncDate
from decimal import Decimal
from datetime import datetime, timedelta


TEXTS = {
    'uk': {
        'home': 'Головна',
        'reports': 'Звіти',
        'profile': 'Профіль',
        'goals': 'Накопичення',

        'welcome': 'Ласкаво просимо до SmartFinance!',
        'balance': 'Баланс',

        'language': 'Мова',
        'theme': 'Тема',
        'currency': 'Валюта',

        'monthly_limit': 'Місячний ліміт',
        'notifications': 'Сповіщення',

        'save': 'Зберегти',
        'rights': 'Всі права захищені',

        'transactions': 'Транзакції',
        'recent_transactions': 'Останні транзакції',
        'add_transaction': 'Додати транзакцію',
        'no_transactions': 'Транзакції відсутні',

        'income': 'Дохід',
        'expense': 'Витрата',

        'amount': 'Сума',
        'category': 'Категорія',
        'emotion': 'Емоційність витрати',
        'description': 'Опис',

        'add': 'Додати',

        'name': 'Ім’я',
        'photo': 'Фото',
        'change_photo': 'Змінити фото',

        'financial_reports': 'Фінансові звіти',
        'period': 'Період',
        'from_date': 'Від',
        'to_date': 'До',
        'generate_report': 'Створити звіт',

        'expenses_by_category': 'Витрати по категоріях',
        'expenses_by_emotion': 'Витрати по емоціях',
        'income_expense_analysis': 'Аналіз доходів та витрат',

        'financial_goals': 'Фінансові цілі',
        'create_goal': 'Створити ціль',
        'goal_name': 'Назва цілі',
        'target_amount': 'Цільова сума',
        'saved_amount': 'Накопичено',
        'progress': 'Прогрес',
        'estimated_date': 'Орієнтовна дата досягнення',
        'add_money': 'Відкласти гроші'
    },

    'en': {
        'home': 'Home',
        'reports': 'Reports',
        'profile': 'Profile',
        'goals': 'Goals',

        'welcome': 'Welcome to SmartFinance!',
        'balance': 'Balance',

        'language': 'Language',
        'theme': 'Theme',
        'currency': 'Currency',

        'monthly_limit': 'Monthly limit',
        'notifications': 'Notifications',

        'save': 'Save',
        'rights': 'All rights reserved',

        'transactions': 'Transactions',
        'recent_transactions': 'Recent transactions',
        'add_transaction': 'Add transaction',
        'no_transactions': 'No transactions yet',

        'income': 'Income',
        'expense': 'Expense',

        'amount': 'Amount',
        'category': 'Category',
        'emotion': 'Expense emotion',
        'description': 'Description',

        'add': 'Add',

        'name': 'Name',
        'photo': 'Photo',
        'change_photo': 'Change photo',

        'financial_reports': 'Financial reports',
        'period': 'Period',
        'from_date': 'From',
        'to_date': 'To',
        'generate_report': 'Generate report',

        'expenses_by_category': 'Expenses by category',
        'expenses_by_emotion': 'Expenses by emotion',
        'income_expense_analysis': 'Income and expense analysis',

        'financial_goals': 'Financial goals',
        'create_goal': 'Create goal',
        'goal_name': 'Goal name',
        'target_amount': 'Target amount',
        'saved_amount': 'Saved',
        'progress': 'Progress',
        'estimated_date': 'Estimated achievement date',
        'add_money': 'Add money'
    },

    'goal_messages': {
    'uk': {
        'done': 'Ціль успішно досягнута!',
        'almost': 'Залишився останній крок!',
        'close': 'Ви вже майже біля цілі!',
        'good': 'Результат стає все ближчим!',
        'half': 'Половина шляху вже позаду!',
        'start': 'Початок вже покладено!',
        'default': 'Час зробити перший крок!'
    },
    'en': {
        'done': 'Goal completed!',
        'almost': 'Almost there!',
        'close': 'You are very close to your goal!',
        'good': 'Great progress so far!',
        'half': 'Halfway there!',
        'start': 'Great start!',
        'default': 'Time to take the first step!'
    }
}
}

CATEGORIES = [
    {"uk": "Їжа", "en": "Food"},
    {"uk": "Транспорт", "en": "Transport"},
    {"uk": "Одяг", "en": "Clothes"},
    {"uk": "Подарунки", "en": "Gifts"},
    {"uk": "Техніка", "en": "Technology"},
    {"uk": "Розваги", "en": "Entertainment"},
    {"uk": "Освіта", "en": "Education"},
    {"uk": "Здоров'я", "en": "Health"},
    {"uk": "Дім/Комунальні", "en": "Home/Utilities"},
    {"uk": "Подорожі", "en": "Travel"},
    {"uk": "Зв'язок", "en": "Communication"},
    {"uk": "Інше", "en": "Other"}
]

EMOTIONS = [
    {"uk": "Планова", "en": "Planned"},
    {"uk": "Імпульсивна", "en": "Impulsive"},
    {"uk": "Для настрою", "en": "For mood"},
    {"uk": "Святкова/сезонна", "en": "Seasonal"},
    {"uk": "Стресова", "en": "Stress-related"},
    {"uk": "Звичкова/рутинна", "en": "Routine"},
    {"uk": "Нагальна", "en": "Urgent"}
]

CATEGORY_TRANSLATIONS = {
    item['uk']: item['en']
    for item in CATEGORIES
}

EMOTION_TRANSLATIONS = {
    item['uk']: item['en']
    for item in EMOTIONS
}
 # хоум
@login_required
def index(request):
    profile = request.user.profile
    
    if request.method == 'POST':
        type = request.POST.get('type')
        amount = request.POST.get('amount')
        category_name = request.POST.get('category')
        emotion_name = request.POST.get('emotion')
        description = request.POST.get('description')

        try:
            amount = float(amount)
        except (TypeError, ValueError):
            amount = 0

        category, _ = Category.objects.get_or_create(name=category_name)
        emotion, _ = Emotion.objects.get_or_create(name=emotion_name)

        Transaction.objects.create(
            user=request.user,
            type=type,
            category=category,
            emotion=emotion,
            amount=amount,
            description=description
        )

        return redirect('index')

    transactions_qs = Transaction.objects.filter(
    user=request.user
).select_related('category', 'emotion').order_by('-date')

    transactions = list(transactions_qs.values(
        'id',
        'type',
        'amount',
        'description',
        'category__name',
        'emotion__name',
        'date'
    ))

 # обраний місяць 
    month = request.GET.get('month')
    year = request.GET.get('year')

    today = timezone.now()

    try:
        month = int(month) if month else today.month
        year = int(year) if year else today.year
    except (TypeError, ValueError):
        month = today.month
        year = today.year


    start_month = datetime(year, month, 1)

    if month == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month + 1, 1)

    # місячні транзакції
    current_month_transactions = Transaction.objects.filter(
        user=request.user,
        date__gte=start_month,
        date__lt=next_month
    )

    month_income = current_month_transactions.filter(
        type='income'
    ).aggregate(total=Sum('amount'))['total'] or 0

    month_expense = current_month_transactions.filter(
        type='expense'
    ).aggregate(total=Sum('amount'))['total'] or 0

    month_balance = month_income - month_expense


    category_data = defaultdict(float)
    total_expenses = 0

    for t in current_month_transactions.filter(type='expense'):
        name = t.category.name if t.category else 'Other'
        category_data[name] += float(t.amount)
        total_expenses += float(t.amount)

    chart_legend = []

    for category, amount in category_data.items():
        percent = (amount / total_expenses * 100) if total_expenses > 0 else 0

        chart_legend.append({
             'category': category,
             'amount': round(amount, 2),
             'percent': round(percent, 1)
        })

    # баланс до місяця
    previous_balance = Transaction.objects.filter(
        user=request.user,
        date__lt=start_month
    ).aggregate(
        total=Sum(
            Case(
                When(type='income', then=F('amount')),
                When(type='expense', then=-F('amount')),
                output_field=DecimalField()
            )
        )
    )['total'] or 0

    lang = request.session.get('language', 'uk')

    total_balance = previous_balance + month_balance


    translated_categories = [
        c[lang] for c in CATEGORIES
    ]

    translated_emotions = [
        e[lang] for e in EMOTIONS
    ]

    return render(request, 'index.html', {
        'transactions': transactions,
        'month_income': month_income,
        'month_expense': month_expense,
        'month_balance': month_balance,
        'previous_balance': previous_balance,
        'total_balance': total_balance,
        'chart_legend': chart_legend,
        'selected_month': month,
        'selected_year': year,
        't': TEXTS.get(lang, TEXTS['uk']),
        'theme': profile.theme,
        'lang': lang,
        'currency': profile.currency,

        'categories': translated_categories,
        'emotions': translated_emotions,
    })

#категорії
@login_required
def categories_view(request):
    profile = request.user.profile

    categories = Category.objects.all()
    lang = request.session.get('language', 'uk')

    return render(request, 'categories.html', {
        'categories': categories,
        'lang': lang,
        'theme': profile.theme,
        't': TEXTS.get(lang, TEXTS['uk'])
    })


def register(request):

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')

    else:
        form = CustomUserCreationForm()

    lang = request.session.get('language', 'uk')

    return render(request, 'register.html', {
        'form': form,
        'lang': lang,
       
        't': TEXTS.get(lang, TEXTS['uk'])
    })


# профіль
@login_required
def profile_view(request):
    profile = request.user.profile

    if request.method == 'POST':
        profile.name = request.POST.get('name')
        profile.language = request.POST.get('language')
        profile.theme = request.POST.get('theme')
        profile.currency = request.POST.get('currency')

        monthly_limit = request.POST.get('monthly_limit')

        if monthly_limit:
            monthly_limit = monthly_limit.replace(',', '.')
            profile.monthly_limit = monthly_limit
        else:
            profile.monthly_limit = 0

        profile.notifications = 'notifications' in request.POST

        if request.FILES.get('avatar'):
            profile.avatar = request.FILES.get('avatar')

        profile.save()

        request.session['language'] = profile.language
        return redirect('profile')

    lang = request.session.get('language', profile.language)

    return render(request, 'profile.html', {
        'profile': profile,
        'lang': lang,
        'theme': profile.theme,
        't': TEXTS.get(lang, TEXTS['uk'])
    })


# зміна мови
def set_language(request, lang):
    if lang in ['uk', 'en']:
        request.session['language'] = lang

    return redirect(request.META.get('HTTP_REFERER', '/'))



# цілі
@login_required
def goals_view(request):

    profile = request.user.profile

    if request.method == 'POST':

        action = request.POST.get('action')

        #створення цілі
        if action == 'create_goal':

            title = request.POST.get('title')
            target_amount = request.POST.get('target_amount')

            try:
                if title and target_amount:
                    Goal.objects.create(
                        user=request.user,
                        title=title,
                        target_amount=Decimal(str(target_amount)),
                        saved_amount=Decimal('0')
                    )
            except (InvalidOperation, ValueError):
                pass

        # додавання грошей
        elif action == 'add_money':

            goal_id = request.POST.get('goal_id')
            amount = request.POST.get('amount')

            try:
                goal = Goal.objects.get(
                    id=goal_id,
                    user=request.user
                )

                amount = Decimal(str(amount))

                if amount <= 0:
                    return redirect('goals')

                goal.saved_amount += amount
                goal.save()

            
                category, _ = Category.objects.get_or_create(
                    name='Накопичення'
                )

                emotion, _ = Emotion.objects.get_or_create(
                    name='Планова'
                )

                Transaction.objects.create(
                    user=request.user,
                    type='expense',
                    category=category,
                    emotion=emotion,
                    amount=amount,
                    description=f'Відкладено на ціль: {goal.title}'
                )

            except (Goal.DoesNotExist, InvalidOperation, ValueError):
                pass

        # видалення цілі
        elif action == 'delete_goal':

            goal_id = request.POST.get('goal_id')

            try:
                Goal.objects.get(
                    id=goal_id,
                    user=request.user
                ).delete()

            except Goal.DoesNotExist:
                pass

        return redirect('goals')
    

    goals = Goal.objects.filter(user=request.user)

    lang = request.session.get('language', profile.language)
    text = TEXTS.get(lang, TEXTS['uk'])
    messages = TEXTS['goal_messages'].get(lang, TEXTS['goal_messages']['uk'])

    for goal in goals:
        try:
            if goal.target_amount and goal.target_amount > 0:
                goal.progress_percent = round(
                    float(goal.saved_amount) / float(goal.target_amount) * 100,
                    2
                )
            else:
                goal.progress_percent = 0
        except:
            goal.progress_percent = 0

        if goal.progress_percent >= 100:
            goal.message = messages['done']
        elif goal.progress_percent >= 90:
            goal.message = messages['almost']
        elif goal.progress_percent >= 80:
            goal.message = messages['close']
        elif goal.progress_percent >= 50:
            goal.message = messages['half']
        elif goal.progress_percent >= 10:
            goal.message = messages['start']
        else:
            goal.message = messages['default']

    return render(request, 'goals.html', {
        'goals': goals,
        'lang': lang,
        'theme': profile.theme,
        'currency': profile.currency,
        't': TEXTS.get(lang, TEXTS['uk'])
    })



#  редагування транзакций
@login_required
def edit_transaction(request, pk):

    transaction = get_object_or_404(
        Transaction,
        id=pk,
        user=request.user
    )

    if request.method == "POST":

        transaction.type = request.POST.get("type")
        transaction.amount = request.POST.get("amount")
        transaction.description = request.POST.get("description")

        category_name = request.POST.get("category")
        emotion_name = request.POST.get("emotion")

        transaction.category, _ = Category.objects.get_or_create(
            name=category_name
        )

        if emotion_name:
            transaction.emotion, _ = Emotion.objects.get_or_create(
                name=emotion_name
            )

        transaction.save()

        return redirect("index")

    return redirect("index")

@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, id=pk, user=request.user)

    if request.method == 'POST':
        transaction.delete()

    return redirect('index')


@login_required
def transactions_view(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')

    return render(request, 'transactions.html', {
        'transactions': transactions
    })



  # звіти
@login_required
def reports_view(request):

    profile = request.user.profile

    lang = request.session.get('language', profile.language)

    all_transactions = Transaction.objects.filter(
    user=request.user
    ).select_related('category', 'emotion')

    transactions = all_transactions

    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    selected_category = request.GET.get('category')
    selected_emotion = request.GET.get('emotion')

# фільтр дати для графіків
   
    if from_date:
        try:
          from_date_obj = datetime.strptime(from_date, '%Y-%m-%d').date()
          transactions = transactions.filter(date__gte=from_date_obj)
        except ValueError:
          pass

    if to_date:
        try:
          to_date_obj = datetime.strptime(to_date, '%Y-%m-%d').date()
          transactions = transactions.filter(date__lte=to_date_obj)
        except ValueError:
           pass
    # фільтр категорій

    if selected_category:
        transactions = transactions.filter(
            category__name=selected_category
        )

    # фільтр емоцій

    if selected_emotion:
        transactions = transactions.filter(
            emotion__name=selected_emotion
        )

    # сумма

    total_income = transactions.filter(type='income').aggregate(
       total=Sum('amount')
    )['total'] or 0

    total_expense = transactions.filter(type='expense').aggregate(
      total=Sum('amount')
    )['total'] or 0

    balance = total_income - total_expense

# місячний ліміт 
    monthly_limit = profile.monthly_limit or 0

    limit_used_amount = transactions.filter(type='expense').aggregate(
        total=Sum('amount')
    )['total'] or 0

    limit_used_percent = 0

    if monthly_limit > 0:
        limit_used_percent = round(
            (float(limit_used_amount) / float(monthly_limit)) * 100,
            1
         )
        if limit_used_percent > 100:
            limit_used_percent = 100

# діаграма по категорім

    category_expenses = defaultdict(float)

    for t in transactions.filter(type='expense'):
         if t.category:
            name = (
                CATEGORY_TRANSLATIONS.get(t.category.name, t.category.name)
                if lang == 'en'
                else t.category.name
            )
         else:
            name = 'Other'

         category_expenses[name] += float(t.amount)

    pie_labels = list(category_expenses.keys())
    pie_values = list(category_expenses.values())

# діаграма дохід/витрат

    chart_transactions = transactions.order_by('date')

    income_data = defaultdict(float)
    expense_data = defaultdict(float)

    for transaction in chart_transactions:

        day = transaction.date.strftime('%d.%m')

        if transaction.type == 'income':
            income_data[day] += float(transaction.amount)

        elif transaction.type == 'expense':
            expense_data[day] += float(transaction.amount)

    all_days = sorted(
        set(list(income_data.keys()) + list(expense_data.keys()))
    )

    income_chart = []
    expense_chart = []

    for day in all_days:
        income_chart.append(income_data.get(day, 0))
        expense_chart.append(expense_data.get(day, 0))


# діаграма по емоціям

    emotion_totals = transactions.filter(
        type='expense'
    ).values(
        'emotion__name'
    ).annotate(
        total=Sum('amount')
    ).order_by('-total')

    emotion_labels = []
    emotion_values = []

    for item in emotion_totals:
        emotion_labels.append(item['emotion__name'] or 'Unknown')
        emotion_values.append(float(item['total']))



        # статистика

    top_category_data = transactions.filter(
        type='expense'
    ).values(
       'category__name'
    ).annotate(
        total=Sum('amount')
    ).order_by('-total').first()

    top_category = (
        top_category_data['category__name']
        if top_category_data else '-'
    )

    top_emotion_data = transactions.filter(
        type='expense'
    ).values(
        'emotion__name'
    ).annotate(
        total=Sum('amount')
    ).order_by('-total').first()

    top_emotion = (
        top_emotion_data['emotion__name']
        if top_emotion_data else '-'
    )

    expense_transactions = transactions.filter(type='expense')

    transactions_count = transactions.count()

    if expense_transactions.exists():
        average_expense = round(
            total_expense / expense_transactions.count(),
            2
        )
    else:
        average_expense = 0

# діаграма накопичувальний баланс

    daily = defaultdict(lambda: {'income': 0, 'expense': 0})

    for t in transactions.order_by('date'):
        day = t.date.strftime('%d.%m')

        if t.type == 'income':
            daily[day]['income'] += float(t.amount)
        else:
            daily[day]['expense'] += float(t.amount)

    all_days_sorted = sorted(daily.keys())

    cumulative_balance = []
    running = 0

    for day in all_days_sorted:
        running += daily[day]['income']
        running -= daily[day]['expense']
        cumulative_balance.append(running)
       
     
    

    return render(request, 'reports.html', {

        'lang': lang,
        'theme': profile.theme,
        'currency': profile.currency,
        't': TEXTS.get(lang, TEXTS['uk']),

        # фільтр
        'from_date': from_date,
        'to_date': to_date,

        'selected_category': selected_category,
        'selected_emotion': selected_emotion,

        # список
        'categories': Category.objects.filter(
           transaction__user=request.user,
           transaction__type='expense'
        ).distinct().order_by('name'),

        'emotions': Emotion.objects.filter(
            transaction__user=request.user
        ).distinct().order_by('name'),


         # дата
        'transactions': transactions,

        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,

        'pie_labels': json.dumps(pie_labels),
        'pie_values': json.dumps(pie_values),

        'emotion_chart_labels': json.dumps(emotion_labels),
        'emotion_chart_values': json.dumps(emotion_values),

        'chart_labels': json.dumps(all_days),

        'income_chart': json.dumps(income_chart),
        'expense_chart': json.dumps(expense_chart),

        'top_category': top_category,
        'top_emotion': top_emotion,
        'average_expense': average_expense,
        'transactions_count': transactions_count,

        'cumulative_labels': json.dumps(all_days_sorted),
        'cumulative_balance': json.dumps(cumulative_balance),

        'monthly_limit': monthly_limit,
        'limit_used_percent': limit_used_percent,
        'limit_used_amount': limit_used_amount,
    })