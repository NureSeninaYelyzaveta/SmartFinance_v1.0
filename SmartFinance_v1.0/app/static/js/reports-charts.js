const reportTranslations = {
    en: {
        categories: {
            'Їжа': 'Food',
            'Транспорт': 'Transport',
            'Одяг': 'Clothes',
            'Подарунки': 'Gifts',
            'Техніка': 'Tech',
            'Розваги': 'Entertainment',
            'Освіта': 'Education',
            "Здоров'я": 'Health',
            'Дім/Комунальні': 'Home/Bills',
            'Інше': 'Other'
        },
        emotions: {
            'Планова': 'Planned',
            'Імпульсивна': 'Impulsive',
            'Для настрою': 'For mood',
            'Святкова/сезонна': 'Seasonal',
            'Стресова': 'Stress-related',
            'Звичкова/рутинна': 'Routine',
            'Нагальна': 'Urgent'
        }
    },

    uk: {
        categories: {
            'Food': 'Їжа',
            'Transport': 'Транспорт',
            'Clothes': 'Одяг',
            'Gifts': 'Подарунки',
            'Tech': 'Техніка',
            'Entertainment': 'Розваги',
            'Education': 'Освіта',
            'Health': "Здоров'я",
            'Home/Bills': 'Дім/Комунальні',
            'Other': 'Інше'
        },
        emotions: {
            'Planned': 'Планова',
            'Impulsive': 'Імпульсивна',
            'For mood': 'Для настрою',
            'Seasonal': 'Святкова/сезонна',
            'Stress-related': 'Стресова',
            'Routine': 'Звичкова/рутинна',
            'Urgent': 'Нагальна'
        }
    }
};


function renderIncomeExpenseChart(labels, incomeData, expenseData) {     // діаграма дохід/витрати
    const ctx = document.getElementById('incomeExpenseChart');

    if (!ctx) return;

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Income',
                    data: incomeData,
                    borderColor: 'green',
                    fill: false
                },
                {
                    label: 'Expenses',
                    data: expenseData,
                    borderColor: 'red',
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: true }
            }
        }
    });
}

//діаграма витрат по категоріям
function renderCategoryPieChart(labels, values) {
    const ctx = document.getElementById('categoryPieChart');
    if (!ctx) return;

    const total = values.reduce((a, b) => a + b, 0);

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: [
                    '#e78146',
                    '#7fbae2',
                    '#6dc246',
                    '#149e9e',
                    'rgb(76, 33, 160)',
                    '#e9d062',
                    '#e285bc',
                    '#7a72e0',
                    '#5b9e0f'
                ],
                borderWidth: 2
            }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '65%',

            layout: {
                padding: {
                    left: 100,
                    right: 20
                }
            },

            plugins: {

                legend: {
                    position: 'left',
                    align: 'center',
                    fullSize: false,

                    labels: {
                        boxWidth: 18,
                        boxHeight: 14,
                        padding: 18,
                        font: {
                            size: 15,
                            weight: '600'
                        },
                        color: '#333',

                        generateLabels: function (chart) {
                            const data = chart.data;
                            const dataset = data.datasets[0];

                            const total = dataset.data.reduce((a, b) => a + b, 0);

                            return data.labels.map((label, i) => {
                                const value = dataset.data[i];
                                const percent = total ? ((value / total) * 100).toFixed(1) : 0;

                                return {
                                    text: `${label} — ${value} (${percent}%)`,
                                    fillStyle: dataset.backgroundColor[i],
                                    strokeStyle: dataset.backgroundColor[i],
                                    index: i
                                };
                            });
                        }
                    }
                },

                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const value = context.raw;
                            const percent = total ? ((value / total) * 100).toFixed(1) : 0;
                            return `${context.label}: ${value} (${percent}%)`;
                        }
                    }
                }
            }
        }
    });
}

// діаграма витрат по емоціям
function renderEmotionPieChart(labels, values) {
    const ctx = document.getElementById('emotionPieChart');

    if (!ctx) return;

    const total = values.reduce((a, b) => a + b, 0);

   
    new Chart(ctx, {
        type: 'doughnut',

        data: {
            labels: labels,

            datasets: [{
                data: values,

                backgroundColor: [
                    '#ff6384',
                    '#36a2eb',
                    '#ffce56',
                    '#4bc0c0',
                    '#9966ff',
                    '#ff9f40',
                    '#8bc34a'
                ],

                borderWidth: 2
            }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '65%',

            layout: {
                padding: {
                    left: 100,
                    right: 20
                }
            },

            plugins: {

                legend: {
                    position: 'left',
                    align: 'center',
                    fullSize: false,

                    labels: {
                        boxWidth: 18,
                        boxHeight: 14,
                        padding: 18,

                        font: {
                            size: 15,
                            weight: '600'
                        },

                        color: '#333',

                        generateLabels: function (chart) {

                          const data = chart.data;
                        const dataset = data.datasets[0];

                        const total = dataset.data.reduce((a, b) => a + b, 0);

                        return data.labels.map((label, i) => {
                           const value = dataset.data[i];
                              const percent = total ? ((value / total) * 100).toFixed(1) : 0;

                          return {
                         text: `${label} — ${value} (${percent}%)`,
                         fillStyle: dataset.backgroundColor[i],
                         strokeStyle: dataset.backgroundColor[i],
                         index: i
                           };
                            });
                        }
                    }
                },

                tooltip: {
                    callbacks: {
                        label: function (context) {

                            const value = context.raw;

                            const percent = total
                                ? ((value / total) * 100).toFixed(1)
                                : 0;

                            return `${context.label}: ${value} (${percent}%)`;
                        }
                    }
                }
            }
        }
    });
}


// накопичувальний баланс
function renderCumulativeChart(labels, values) {

    const ctx = document.getElementById('cumulativeChart');

    if (!ctx) return;

    new Chart(ctx, {
        type: 'line',

        data: {
            labels: labels,

            datasets: [{
                label: 'Cumulative Balance',
                data: values,

                borderColor: '#6b1fb3',
                backgroundColor: 'rgba(107, 31, 179, 0.15)',

                tension: 0.4,
                fill: true,
                pointRadius: 4
            }]
        },

        options: {
            responsive: true,

            plugins: {
                legend: {
                    labels: {
                        boxWidth: 12,
                        padding: 18
                    }
                }
            },

            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });
}

function translateReportValues() {
    const lang = window.currentLang || 'uk';
    const t = reportTranslations[lang];

    if (!t) return;

    const categoryEl = document.querySelector('[data-report="category"]');
    if (categoryEl) {
        const key = categoryEl.dataset.value;
        categoryEl.textContent = t.categories[key] || key;
    }

    const emotionEl = document.querySelector('[data-report="emotion"]');
    if (emotionEl) {
        const key = emotionEl.dataset.value;
        emotionEl.textContent = t.emotions[key] || key;
    }
}
translateReportValues();
