 document.addEventListener('DOMContentLoaded', () => {

const months = window.currentLang === 'en'
    ? [
        'January', 'February', 'March', 'April',
        'May', 'June', 'July', 'August',
        'September', 'October', 'November', 'December'
    ]
    : [
        'Січень', 'Лютий', 'Березень', 'Квітень',
        'Травень', 'Червень', 'Липень', 'Серпень',
        'Вересень', 'Жовтень', 'Листопад', 'Грудень'
    ];

    const categoryLabels = {
    en: {
        'Зарплата': 'Salary',
        'Бізнес': 'Business',
        'Подарунки': 'Gifts',
        'Інше': 'Other',
        'Їжа': 'Food',
        'Транспорт': 'Transport',
        'Одяг': 'Clothes',
        'Техніка': 'Tech',
        'Розваги': 'Entertainment',
        'Освіта': 'Education',
        'Здоров\'я': 'Health',
        'Дім/Комунальні': 'Home/Bills',
         'Накопичення': 'Savings'
    },

    uk: {
        'Зарплата': 'Зарплата',
        'Бізнес': 'Бізнес',
        'Подарунки': 'Подарунки',
        'Інше': 'Інше',
        'Їжа': 'Їжа',
        'Транспорт': 'Транспорт',
        'Одяг': 'Одяг',
        'Техніка': 'Техніка',
        'Розваги': 'Розваги',
        'Освіта': 'Освіта',
        'Здоров\'я': 'Здоров\'я',
        'Дім/Комунальні': 'Дім/Комунальні',
        'Накопичення': 'Накопичення'
    }
};

const uiText = {
    en: {
        previousBalance: "Previous balance",
        income: "Monthly income",
        expense: "Monthly expenses",
        total: "Total balance"
    },
    uk: {
        previousBalance: "Залишок з минулих місяців",
        income: "Дохід за місяць",
        expense: "Витрати за місяць",
        total: "Загальний баланс"
    }
};

function updateSummaryTexts() {
    const lang = window.currentLang || 'uk';
    const t = uiText[lang] || uiText.uk;

    const prevTitle = document.querySelector('.summary-card.neutral .summary-title');
    const incomeTitle = document.querySelector('.summary-card.income .summary-title');
    const expenseTitle = document.querySelector('.summary-card.expense .summary-title');
    const totalTitle = document.querySelector('.summary-card.total .summary-title');

    if (prevTitle) prevTitle.textContent = t.previousBalance;
    if (incomeTitle) incomeTitle.textContent = t.income;
    if (expenseTitle) expenseTitle.textContent = t.expense;
    if (totalTitle) totalTitle.textContent = t.total;
} 

    let currentDate = new Date();
    let chart = null;

    
    const prev = document.querySelector('.prev-month');
    const next = document.querySelector('.next-month');
    const monthYear = document.querySelector('.month-year');
    const chartCanvas = document.getElementById('transactionsChart');
 

   const transactionsJSON = document.getElementById('transactions');

let transactions = [];

if (transactionsJSON) {
    try {
        transactions = JSON.parse(transactionsJSON.textContent || '[]');
    } catch (e) {
        console.warn('JSON error', e);
        transactions = [];
    }
}

    
function updateChart() {

    if (!chartCanvas || typeof Chart === 'undefined') return;

    const monthly = getMonthlyData();

    const totals = getTotals(monthly);

    const previousBalance = getPreviousBalance();
    const finalBalance =
        previousBalance +
        totals.income -
        totals.expense;


    const categories = getCategoryData(monthly);

    const incomeEl = document.getElementById('incomeSum');
    const expenseEl = document.getElementById('expenseSum');
    const totalEl = document.getElementById('totalSum');

    const previousEl = document.getElementById('previousBalance');
    const finalEl = document.getElementById('finalBalance');

    if (incomeEl) incomeEl.textContent = totals.income.toFixed(2);
    if (expenseEl) expenseEl.textContent = totals.expense.toFixed(2);
    if (totalEl) totalEl.textContent = totals.total.toFixed(2);

    if (previousEl) {
        previousEl.textContent = previousBalance.toFixed(2);
}

    if (finalEl) {
        finalEl.textContent = finalBalance.toFixed(2);
}

    if (chart) chart.destroy();


    chart = new Chart(chartCanvas, {
        type: 'doughnut',
        data: {
            labels: Object.keys(categories),
            datasets: [{
                data: Object.values(categories),
               backgroundColor: [
    '#4eabd6',
    '#e4806c', 
    '#dfc252', 
    '#9282d3',
    '#52b96c', 
     
    '#c46599',
    '#39c1d3', 
    '#56d4ae',
    '#dfb630'  
]
            }]
        },
        options: {
            cutout: '65%',
            plugins: {
               legend: {
                    display: false
            }
}     
        }

            });
            renderLegend(categories);
}

    function updateMonth() {
        if (!monthYear) return;

        monthYear.textContent =
            months[currentDate.getMonth()] +
            ' ' +
            currentDate.getFullYear();

            
        updateChart();
        renderTransactionsList();
    }

    if (prev && next && monthYear) {

        prev.addEventListener('click', () => {
            currentDate.setMonth(currentDate.getMonth() - 1);
            updateMonth();
        });

        next.addEventListener('click', () => {
            currentDate.setMonth(currentDate.getMonth() + 1);
            updateMonth();
        });


        updateMonth();
    }


    const modal = document.getElementById('transactionModal');
    const openBtn = document.getElementById('openModal');
    const closeBtn = document.querySelector('#transactionModal .close');

    if (openBtn && modal) {
        openBtn.addEventListener('click', () => {
            modal.style.display = 'flex';
        });
    }

    if (closeBtn && modal) {
        closeBtn.addEventListener('click', () => {
            modal.style.display = 'none';
        });
    }

    window.addEventListener('click', (e) => {
        if (modal && e.target === modal) {
            modal.style.display = 'none';
        }
    });


    function renderTransactionsList() {

    const items = document.querySelectorAll('.transaction-item');
    const container = document.querySelector('.transaction-list');

    const month = currentDate.getMonth();
    const year = currentDate.getFullYear();

    let visibleCount = 0;

    items.forEach(item => {

        const dateStr = item.getAttribute('data-date');
        if (!dateStr) return;

        const date = new Date(dateStr);

        const match =
            date.getMonth() === month &&
            date.getFullYear() === year;

        item.style.display = match ? '' : 'none';

        if (match) visibleCount++;
    });


    let emptyMsg = document.querySelector('.empty-message');

    if (visibleCount === 0) {

        if (!emptyMsg) {
            emptyMsg = document.createElement('p');
            emptyMsg.className = 'empty-message';

            emptyMsg.textContent =
                window.currentLang === 'en'
                    ? 'No transactions for this month'
                    : 'Тут поки що немає транзакцій';

            container.appendChild(emptyMsg);
        }

    } else {
        if (emptyMsg) emptyMsg.remove();
    }
}


    window.openEditModal = function (id, type, amount, category, emotion, description) {

        const modal = document.getElementById('editModal');
        const form = document.getElementById('editForm');

        if (!modal || !form) return;

        form.action = `/transaction/edit/${id}/`;

        const amountEl = document.getElementById('edit_amount');
        const categoryEl = document.getElementById('edit_category');
        const emotionEl = document.getElementById('edit_emotion');
        const descriptionEl = document.getElementById('edit_description');

        const incomeEl = document.getElementById('edit_income');
        const expenseEl = document.getElementById('edit_expense');

        if (amountEl) amountEl.value = amount || '';
        if (categoryEl) categoryEl.value = category || '';
        if (emotionEl) emotionEl.value = emotion || '';
        if (descriptionEl) descriptionEl.value = description || '';

        if (incomeEl) incomeEl.checked = type === 'income';
        if (expenseEl) expenseEl.checked = type === 'expense';

        modal.style.display = 'flex';
    };

    window.closeEditModal = function () {
        const modal = document.getElementById('editModal');
        if (modal) modal.style.display = 'none';
    };


    function getMonthlyData() {
    const month = currentDate.getMonth();
    const year = currentDate.getFullYear();

    return transactions.filter(t => {
        const d = new Date(t.date);
        return d.getMonth() === month && d.getFullYear() === year;
    });
}

function getTotals(monthly) {
    let income = 0;
    let expense = 0;

    monthly.forEach(t => {
        const amount = Number(t.amount) || 0;

        if (t.type === 'income') income += amount;
        if (t.type === 'expense') expense += amount;
    });

    return { income, expense, total: income - expense };
}

function getPreviousBalance() {

    const currentMonth = currentDate.getMonth();
    const currentYear = currentDate.getFullYear();

    let balance = 0;

    transactions.forEach(t => {

        const d = new Date(t.date);

        const isBefore =
            d.getFullYear() < currentYear ||
            (
                d.getFullYear() === currentYear &&
                d.getMonth() < currentMonth
            );

        if (!isBefore) return;

        const amount = Number(t.amount) || 0;

        if (t.type === 'income') {
            balance += amount;
        }

        if (t.type === 'expense') {
            balance -= amount;
        }
    });

    return balance;
}


function getCategoryData(monthly) {
    const categories = {};

    monthly.forEach(t => {
        if (t.type !== 'expense') return;

        const cat = t.category__name || 'Інше';
        const amount = Number(t.amount) || 0;

        categories[cat] = (categories[cat] || 0) + amount;
    });

    return categories;
}


function renderLegend(categories) {

    const legend = document.getElementById('chartLegend');
    if (!legend) return;

    const total = Object.values(categories)
        .reduce((sum, val) => sum + val, 0);

    const colors = [
       '#4eabd6',
    '#e4806c', 
    '#dfc252', 
    '#9282d3',
    '#52b96c', 
     
    '#c46599',
    '#39c1d3', 
    '#56d4ae',
    '#dfb630'  
    ];

    legend.innerHTML = '';

    Object.entries(categories).forEach(([name, value], index) => {

        const percent = total ? ((value / total) * 100).toFixed(1) : 0;
        const color = colors[index % colors.length];

        const item = document.createElement('div');
        item.className = 'legend-item';

        item.innerHTML = `
            <div class="legend-left">
                <span class="legend-dot" style="background:${color}"></span>
               <span class="legend-name">
    ${(categoryLabels[window.currentLang]?.[name] || name)}
</span>
            </div>

            <div class="legend-right">
                <span class="legend-amount">${value.toFixed(2)}</span>
                <span class="legend-percent">(${percent}%)</span>
            </div>
        `;

        legend.appendChild(item);
    });
}

requestAnimationFrame(() => {
    if (typeof updateSummaryTexts === 'function') {
        updateSummaryTexts();
    }
});

});