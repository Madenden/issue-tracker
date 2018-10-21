let endpoint = '/chart/data/';
let labels = [];
let tickets_qty = [];
$.ajax({
    method: "GET",
    url: endpoint,
    success: function(data) {
        labels = data.labels;
        feature_ticket_qty = data.feature_ticket_qty;
        bug_tickets_qty = data.bug_tickets_qty;
        days = data.days;
        months = data.months;
        bugs_per_week = data.bugs_per_week;
        features_per_week = data.features_per_week;
        bugs_per_month = data.bugs_per_month;
        feature_per_month = data.feature_per_month;
        bugs_top_five_title = data.bugs_top_five_title;
        bugs_top_five_upvotes_count = data.bugs_top_five_upvotes_count;
        features_top_five_title = data.features_top_five_title;
        features_top_five_upvotes_count = data.features_top_five_upvotes_count;
        
        let ctxPieChart = document.getElementById('pieChart').getContext('2d');
        let pieChart = new Chart(ctxPieChart, {
            type: 'pie',
            data: {
                labels: bugs_top_five_title,
                datasets: [{
                        label: bugs_top_five_title,
                        data: bugs_top_five_upvotes_count,
                        backgroundColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)',
                        ],
                        borderColor: [
                            'rgba(255,255,255,1)'
                        ]
                    }
                ]
            },
            options: {
                title: {
                    display: true,
                    text: 'Top 5 Most-Upvoted Bug Tickets'
                }
            }
        });
        
        let ctxPieChartFeature = document.getElementById('pieChart_feature').getContext('2d');
        let pieChart_feature = new Chart(ctxPieChartFeature, {
            type: 'pie',
            data: {
                labels: features_top_five_title,
                datasets: [{
                        label: features_top_five_title,
                        data: features_top_five_upvotes_count,
                        backgroundColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)',
                        ],
                        borderColor: [
                            'rgba(255,255,255,1)'
                        ]
                    }
                ]
            },
            options: {
                title: {
                    display: true,
                    text: 'Top 5 Most-Upvoted Feature Tickets'
                }
            }
        });
        
        let ctx = document.getElementById('myChart').getContext('2d');
        let myChart = new Chart(ctx, {
            type: 'horizontalBar',
            data: {
                labels: days,
                datasets: [{
                        label: labels[0],
                        data: bug_tickets_qty,
                        backgroundColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(255, 99, 132, 1)',
                            'rgba(255, 99, 132, 1)',
                            'rgba(255, 99, 132, 1)',
                            'rgba(255, 99, 132, 1)',
                            'rgba(255, 99, 132, 1)',
                            'rgba(255, 99, 132, 1)',
                        ],
                        borderColor: [
                            'rgba(255,255,255,1)'
                        ]
                    },
                    {
                        label: labels[1],
                        data: feature_ticket_qty,
                        backgroundColor: [
                            'rgba(54, 162, 235, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(54, 162, 235, 1)',
                        ],
                        borderColor: [
                            'rgba(255,255,255,1)'
                        ]
                    }
                ]
            },
            options: {
                title: {
                    display: true,
                    text: 'Tickets Have Been Created on Daily Base ( the report show data from Yesterday )'
                }
            }
        });
        
        let ctx_weekly = document.getElementById('myChart_weekly').getContext('2d');
        let myChart_weekly = new Chart(ctx_weekly, {
            type: 'horizontalBar',
            data: {
                labels: ['week1', 'week2', 'week3', 'week4'],
                datasets: [{
                        label: labels[0],
                        data: bugs_per_week,
                        backgroundColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(255, 99, 132, 1)',
                            'rgba(255, 99, 132, 1)',
                            'rgba(255, 99, 132, 1)'
                        ],
                        borderColor: [
                            'rgba(255,255,255,1)'
                        ]
                    },
                    {
                        label: labels[1],
                        data: features_per_week,
                        backgroundColor: [
                            'rgba(54, 162, 235, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(54, 162, 235, 1)'
                        ],
                        borderColor: [
                            'rgba(255,255,255,1)'
                        ]
                    }
                ]
            },
            options: {
                title: {
                    display: true,
                    text: 'Tickets Have Been Created on Weekly Base ( the report show data from Yesterday )'
                }
            }
        });
        
        let ctx2 = document.getElementById('myChart2').getContext('2d');
        let myChart2 = new Chart(ctx2, {
            type: 'horizontalBar',
            data: {
                labels: months,
                datasets: [{
                        label: labels[0],
                        data: bugs_per_month,
                        backgroundColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(255, 99, 132, 1)',
                            'rgba(255, 99, 132, 1)',
                            'rgba(255, 99, 132, 1)',
                            'rgba(255, 99, 132, 1)',
                            'rgba(255, 99, 132, 1)',
                            'rgba(255, 99, 132, 1)',
                            'rgba(255, 99, 132, 1)',
                            'rgba(255, 99, 132, 1)',
                            'rgba(255, 99, 132, 1)',
                            'rgba(255, 99, 132, 1)',
                            'rgba(255, 99, 132, 1)',
                        ],
                        borderColor: [
                            'rgba(255,255,255,1)'
                        ]
                    },
                    {
                        label: labels[1],
                        data: feature_per_month,
                        backgroundColor: [
                            'rgba(54, 162, 235, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(54, 162, 235, 1)',
                        ],
                        borderColor: [
                            'rgba(255,255,255,1)'
                        ]
                    }
                ]
            },
            options: {
                title: {
                    display: true,
                    text: 'Tickets Have Been Created on Monthly Base'
                }
            }
        });
    },
    error: function(error_data) {
        console.log("error");
        console.log(error_data);
    }
});
