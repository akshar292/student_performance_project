// StudentIQ Frontend Logic with Chart.js & Flask REST APIs

document.addEventListener("DOMContentLoaded", () => {
    // Global chart instances
    let chartPassFailInstance = null;
    let chartCityPerfInstance = null;
    let chartAttendanceInstance = null;
    let chartStudyInstance = null;
    let chartFeatureInstance = null;
    let chartRadarInstance = null;

    // Cache current students data for search table & radar modal
    let cachedStudents = [];

    // DOM Elements
    const navButtons = document.querySelectorAll(".nav-btn");
    const tabContents = document.querySelectorAll(".tab-content");
    const pageTitle = document.getElementById("pageTitle");
    const pageSubtitle = document.getElementById("pageSubtitle");

    // ==========================================
    // DASHBOARD OPEN / CLOSE TOGGLE
    // ==========================================

    const dashboardSection =
        document.getElementById("tab-dashboard");

    if (dashboardSection) {

        const header =
            document.querySelector("header");

        if (
            header &&
            !document.getElementById("dashboardToggleBtn")
        ) {

            const headerActions =
                header.querySelector(
                    ".flex.items-center.gap-3"
                );

            if (headerActions) {

                const dashboardToggleBtn =
                    document.createElement("button");

                dashboardToggleBtn.id =
                    "dashboardToggleBtn";

                dashboardToggleBtn.type =
                    "button";

                dashboardToggleBtn.className =
                    "flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-brand-500/10 border border-brand-500/30 text-brand-300 text-xs font-bold hover:bg-brand-500/20 transition-all";

                dashboardToggleBtn.innerHTML = `
                <i
                    id="dashboardToggleIcon"
                    class="fa-solid fa-eye-slash"
                ></i>

                <span
                    id="dashboardToggleText"
                >
                    Close Dashboard
                </span>
            `;

                headerActions.insertBefore(
                    dashboardToggleBtn,
                    headerActions.firstElementChild
                );


                // ==================================
                // BUTTON CLICK
                // ==================================

                dashboardToggleBtn.addEventListener(
                    "click",
                    function () {

                        const isHidden =
                            dashboardSection.classList.contains(
                                "hidden"
                            );


                        // ==============================
                        // OPEN DASHBOARD
                        // ==============================

                        if (isHidden) {

                            dashboardSection.classList.remove(
                                "hidden"
                            );

                            dashboardSection.classList.add(
                                "block"
                            );


                            // Activate Dashboard navigation

                            navButtons.forEach(
                                function (button) {

                                    button.classList.remove(
                                        "active"
                                    );

                                    button.classList.add(
                                        "text-slate-400"
                                    );

                                }
                            );


                            const dashboardNavButton =
                                document.querySelector(
                                    '.nav-btn[data-tab="dashboard"]'
                                );


                            if (dashboardNavButton) {

                                dashboardNavButton.classList.add(
                                    "active"
                                );

                                dashboardNavButton.classList.remove(
                                    "text-slate-400"
                                );

                            }


                            // Update page title

                            if (
                                pageTitle &&
                                tabMetaData.dashboard
                            ) {

                                pageTitle.textContent =
                                    tabMetaData.dashboard.title;

                                pageSubtitle.textContent =
                                    tabMetaData.dashboard.subtitle;

                            }


                            // Update button

                            document.getElementById(
                                "dashboardToggleText"
                            ).textContent =
                                "Close Dashboard";


                            document.getElementById(
                                "dashboardToggleIcon"
                            ).className =
                                "fa-solid fa-eye-slash";

                        }


                        // ==============================
                        // CLOSE DASHBOARD
                        // ==============================

                        else {

                            dashboardSection.classList.remove(
                                "block"
                            );

                            dashboardSection.classList.add(
                                "hidden"
                            );


                            document.getElementById(
                                "dashboardToggleText"
                            ).textContent =
                                "Open Dashboard";


                            document.getElementById(
                                "dashboardToggleIcon"
                            ).className =
                                "fa-solid fa-eye";

                        }

                    }
                );

            }

        }

    }

    // Global Filter Elements
    const filterCity = document.getElementById("filterCity");
    const filterGenderGroup = document.getElementById("filterGenderGroup");
    const filterMinAge = document.getElementById("filterMinAge");
    const filterMaxAge = document.getElementById("filterMaxAge");
    const ageRangeVal = document.getElementById("ageRangeVal");
    const filterResult = document.getElementById("filterResult");
    const applyFiltersBtn = document.getElementById("applyFiltersBtn");
    const resetFiltersBtn = document.getElementById("resetFiltersBtn");

    // Sidebar Mobile Toggle
    const openSidebarBtn = document.getElementById("openSidebarBtn");
    const closeSidebarBtn = document.getElementById("closeSidebarBtn");
    const sidebar = document.getElementById("sidebar");

    if (openSidebarBtn && sidebar) {
        openSidebarBtn.addEventListener("click", () => sidebar.classList.remove("-translate-x-full"));
    }
    if (closeSidebarBtn && sidebar) {
        closeSidebarBtn.addEventListener("click", () => sidebar.classList.add("-translate-x-full"));
    }

    // Tab Navigation Configuration
    const tabMetaData = {
        dashboard: { title: "Academic Performance Intelligence", subtitle: "Real-time overview & KPI metrics of student academic standing" },
        analytics: { title: "Academic Factor Analytics", subtitle: "Deep-dive into attendance, study habits, correlation matrix, & ML feature importances" },
        prediction: { title: "AI Score & Pass/Fail Predictor", subtitle: "Simulate student metrics to predict final grade score and pass probability" },
        students: { title: "Student Performance Directory", subtitle: "Search, filter, and inspect individual student scorecards" },
        sql: { title: "SQL Insights & Query Console", subtitle: "Run pre-packaged analytical queries or custom SQL on the dataset" }
    };

    navButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const targetTab = btn.getAttribute("data-tab");

            navButtons.forEach(b => {
                b.classList.remove("active");
                b.classList.add("text-slate-400");
            });
            btn.classList.add("active");
            btn.classList.remove("text-slate-400");

            tabContents.forEach(content => {
                if (content.id === `tab-${targetTab}`) {
                    content.classList.remove("hidden");
                    content.classList.add("block");
                } else {
                    content.classList.add("hidden");
                    content.classList.remove("block");
                }
            });

            if (tabMetaData[targetTab]) {
                pageTitle.textContent = tabMetaData[targetTab].title;
                pageSubtitle.textContent = tabMetaData[targetTab].subtitle;
            }

            // Close sidebar on mobile after navigating
            if (window.innerWidth < 768 && sidebar) {
                sidebar.classList.add("-translate-x-full");
            }
        });
    });

    // 1. Fetch System Meta (Cities, Genders, Min/Max Age)
    async function loadMeta() {
        try {
            const res = await fetch("/api/meta");
            const data = await res.json();

            // Populate Cities Multi-select
            filterCity.innerHTML = "";
            data.cities.forEach(c => {
                const opt = document.createElement("option");
                opt.value = c;
                opt.textContent = c;
                opt.selected = true;
                filterCity.appendChild(opt);
            });

            // Populate Genders Checkboxes
            filterGenderGroup.innerHTML = "";
            data.genders.forEach(g => {
                const label = document.createElement("label");
                label.className = "flex items-center gap-1.5 cursor-pointer";
                label.innerHTML = `
                    <input type="checkbox" name="genderFilter" value="${g}" checked class="accent-brand-500 rounded">
                    <span>${g}</span>
                `;
                filterGenderGroup.appendChild(label);
            });

            // Age Range Sliders
            filterMinAge.min = data.min_age;
            filterMinAge.max = data.max_age;
            filterMinAge.value = data.min_age;

            filterMaxAge.min = data.min_age;
            filterMaxAge.max = data.max_age;
            filterMaxAge.value = data.max_age;

            updateAgeDisplay();

            // Database connection badge
            const dbText = document.getElementById("dbStatusText");
            const dbBadge = document.getElementById("dbStatusBadge");
            if (data.is_db_connected) {
                dbText.textContent = "MySQL Connected";
                dbBadge.className = "flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold";
            } else {
                dbText.textContent = "Offline Sample Data";
                dbBadge.className = "flex items-center gap-2 px-3 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-semibold";
            }

            // Initial load of data
            fetchDashboardData();
        } catch (err) {
            console.error("Error loading meta options:", err);
        }
    }

    function updateAgeDisplay() {
        let minVal = parseInt(filterMinAge.value);
        let maxVal = parseInt(filterMaxAge.value);
        if (minVal > maxVal) {
            filterMinAge.value = maxVal;
            minVal = maxVal;
        }
        ageRangeVal.textContent = `${minVal} - ${maxVal}`;
    }

    filterMinAge.addEventListener("input", updateAgeDisplay);
    filterMaxAge.addEventListener("input", updateAgeDisplay);

    // Filter Payload Helper
    function getFilterPayload() {
        const selectedCities = Array.from(filterCity.selectedOptions).map(opt => opt.value);
        const genderInputs = document.querySelectorAll('input[name="genderFilter"]:checked');
        const selectedGenders = Array.from(genderInputs).map(i => i.value);

        return {
            cities: selectedCities,
            genders: selectedGenders,
            age_min: parseInt(filterMinAge.value),
            age_max: parseInt(filterMaxAge.value),
            result_filter: filterResult.value
        };
    }

    applyFiltersBtn.addEventListener("click", () => fetchDashboardData());

    resetFiltersBtn.addEventListener("click", () => {
        Array.from(filterCity.options).forEach(opt => opt.selected = true);
        document.querySelectorAll('input[name="genderFilter"]').forEach(i => i.checked = true);
        filterMinAge.value = filterMinAge.min;
        filterMaxAge.value = filterMaxAge.max;
        filterResult.value = "All";
        updateAgeDisplay();
        fetchDashboardData();
    });

    // 2. Fetch Core Dashboard Data & Render Visualizations
    async function fetchDashboardData() {
        try {
            const payload = getFilterPayload();
            const res = await fetch("/api/data", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            const data = await res.json();

            if (data.empty) {
                alert(data.message);
                return;
            }

            // Cache student list
            cachedStudents = data.students || [];

            // Update KPI Cards
            document.getElementById("kpiTotal").textContent = data.summary.total_count.toLocaleString();
            document.getElementById("kpiAvgScore").textContent = data.summary.avg_score;
            document.getElementById("kpiPassPct").textContent = `${data.summary.pass_pct}%`;
            document.getElementById("kpiPassFailCounts").textContent = `${data.summary.passed_count} Passed | ${data.summary.failed_count} Failed`;
            document.getElementById("kpiTopCity").textContent = data.summary.top_city;
            document.getElementById("kpiTopCityScore").textContent = `Avg Score: ${data.summary.top_city_score}`;

            // Render Charts
            renderPassFailChart(data.charts.pass_fail);
            renderCityPerfChart(data.charts.city_stats);
            renderAttendanceChart(data.charts.attendance_scatter);
            renderStudyChart(data.charts.study_hours_scatter);
            renderFeatureChart(data.charts.feature_importances);
            renderCorrelationMatrix(data.charts.correlation);

            // Render Student Directory Table
            renderStudentsTable(cachedStudents);

        } catch (err) {
            console.error("Error fetching dashboard data:", err);
        }
    }

    // Chart 1: Pass vs Fail Doughnut
    function renderPassFailChart(data) {
        const ctx = document.getElementById("chartPassFail").getContext("2d");
        if (chartPassFailInstance) chartPassFailInstance.destroy();

        chartPassFailInstance = new Chart(ctx, {
            type: "doughnut",
            data: {
                labels: ["PASS", "FAIL"],
                datasets: [{
                    data: [data.PASS, data.FAIL],
                    backgroundColor: ["#10b981", "#f43f5e"],
                    borderColor: "#0f172a",
                    borderWidth: 3,
                    hoverOffset: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: "bottom", labels: { color: "#cbd5e1", font: { family: "Plus Jakarta Sans", weight: 600 } } }
                },
                cutout: "70%"
            }
        });
    }

    // Chart 2: City Academic Averages Bar Chart
    function renderCityPerfChart(cityStats) {
        const ctx = document.getElementById("chartCityPerf").getContext("2d");
        if (chartCityPerfInstance) chartCityPerfInstance.destroy();

        const labels = cityStats.map(c => c.city);
        const scores = cityStats.map(c => c.avg_score);

        chartCityPerfInstance = new Chart(ctx, {
            type: "bar",
            data: {
                labels: labels,
                datasets: [{
                    label: "Average Final Score",
                    data: scores,
                    backgroundColor: "rgba(99, 102, 241, 0.7)",
                    borderColor: "#6366f1",
                    borderWidth: 1.5,
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { ticks: { color: "#94a3b8" }, grid: { color: "#1e293b" } },
                    y: { ticks: { color: "#94a3b8" }, grid: { color: "#1e293b" }, min: 0, max: 100 }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }

    // Chart 3: Attendance vs Score Scatter
    function renderAttendanceChart(points) {
        const ctx = document.getElementById("chartAttendanceVsScore").getContext("2d");
        if (chartAttendanceInstance) chartAttendanceInstance.destroy();

        const scatterData = points.map(p => ({
            x: p.attendance,
            y: p.final_score,
            result: p.result
        }));

        chartAttendanceInstance = new Chart(ctx, {
            type: "scatter",
            data: {
                datasets: [{
                    label: "Students",
                    data: scatterData,
                    backgroundColor: scatterData.map(d => d.result === "PASS" ? "rgba(16, 185, 129, 0.6)" : "rgba(244, 63, 94, 0.6)"),
                    pointRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { title: { display: true, text: "Attendance (%)", color: "#94a3b8" }, ticks: { color: "#94a3b8" }, grid: { color: "#1e293b" } },
                    y: { title: { display: true, text: "Final Score", color: "#94a3b8" }, ticks: { color: "#94a3b8" }, grid: { color: "#1e293b" } }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }

    // Chart 4: Study Hours vs Score Scatter
    function renderStudyChart(points) {
        const ctx = document.getElementById("chartStudyVsScore").getContext("2d");
        if (chartStudyInstance) chartStudyInstance.destroy();

        const scatterData = points.map(p => ({
            x: p.study_hours,
            y: p.final_score,
            result: p.result
        }));

        chartStudyInstance = new Chart(ctx, {
            type: "scatter",
            data: {
                datasets: [{
                    label: "Students",
                    data: scatterData,
                    backgroundColor: scatterData.map(d => d.result === "PASS" ? "rgba(6, 182, 212, 0.6)" : "rgba(244, 63, 94, 0.6)"),
                    pointRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { title: { display: true, text: "Daily Study Hours (hrs)", color: "#94a3b8" }, ticks: { color: "#94a3b8" }, grid: { color: "#1e293b" } },
                    y: { title: { display: true, text: "Final Score", color: "#94a3b8" }, ticks: { color: "#94a3b8" }, grid: { color: "#1e293b" } }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }

    // Chart 5: Feature Importances
    function renderFeatureChart(features) {
        const ctx = document.getElementById("chartFeatureImportances").getContext("2d");
        if (chartFeatureInstance) chartFeatureInstance.destroy();

        const labels = features.map(f => f.feature);
        const scoreImp = features.map(f => f.score_importance);
        const classImp = features.map(f => f.class_importance);

        chartFeatureInstance = new Chart(ctx, {
            type: "bar",
            data: {
                labels: labels,
                datasets: [
                    { label: "Regressor (Score)", data: scoreImp, backgroundColor: "rgba(99, 102, 241, 0.8)", borderRadius: 6 },
                    { label: "Classifier (Pass/Fail)", data: classImp, backgroundColor: "rgba(168, 85, 247, 0.8)", borderRadius: 6 }
                ]
            },
            options: {
                indexAxis: "y",
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { ticks: { color: "#94a3b8" }, grid: { color: "#1e293b" } },
                    y: { ticks: { color: "#cbd5e1" }, grid: { color: "#1e293b" } }
                },
                plugins: {
                    legend: { labels: { color: "#cbd5e1" } }
                }
            }
        });
    }

    // Correlation Matrix Table Renderer
    function renderCorrelationMatrix(corrDict) {
        const headerRow = document.getElementById("corrHeader");
        const body = document.getElementById("corrBody");

        const keys = Object.keys(corrDict);
        headerRow.innerHTML = `<th class="p-2 border-r border-slate-700">Metric</th>` + keys.map(k => `<th class="p-2 text-center">${k.replace('_', ' ')}</th>`).join("");

        body.innerHTML = "";
        keys.forEach(rowKey => {
            let tr = document.createElement("tr");
            tr.className = "hover:bg-slate-800/40 transition-colors";
            let rowHtml = `<td class="p-2 font-bold text-slate-300 border-r border-slate-800 uppercase text-[10px]">${rowKey.replace('_', ' ')}</td>`;

            keys.forEach(colKey => {
                const val = corrDict[rowKey][colKey];
                let bgClass = "text-slate-400";
                if (val === 1) bgClass = "text-indigo-400 font-bold";
                else if (val > 0.6) bgClass = "text-emerald-400 font-bold";
                else if (val > 0.3) bgClass = "text-cyan-300";

                rowHtml += `<td class="p-2 text-center ${bgClass}">${val.toFixed(2)}</td>`;
            });

            tr.innerHTML = rowHtml;
            body.appendChild(tr);
        });
    }

    // 3. AI Prediction Form Controls
    const predForm = document.getElementById("predictionForm");
    const inputAttendance = document.getElementById("inputAttendance");
    const inputStudyHours = document.getElementById("inputStudyHours");
    const inputAssignment = document.getElementById("inputAssignment");
    const inputMidterm = document.getElementById("inputMidterm");
    const inputPrevious = document.getElementById("inputPrevious");

    // Dynamic Slider Values Display
    inputAttendance.addEventListener("input", e => document.getElementById("valAttendance").textContent = `${e.target.value}%`);
    inputStudyHours.addEventListener("input", e => document.getElementById("valStudyHours").textContent = `${e.target.value} hrs`);
    inputAssignment.addEventListener("input", e => document.getElementById("valAssignment").textContent = e.target.value);
    inputMidterm.addEventListener("input", e => document.getElementById("valMidterm").textContent = e.target.value);
    inputPrevious.addEventListener("input", e => document.getElementById("valPrevious").textContent = e.target.value);

    predForm.addEventListener("submit", async e => {
        e.preventDefault();

        const payload = {
            attendance: parseFloat(inputAttendance.value),
            study_hours: parseFloat(inputStudyHours.value),
            assignment_score: parseFloat(inputAssignment.value),
            midterm_score: parseFloat(inputMidterm.value),
            previous_score: parseFloat(inputPrevious.value)
        };

        try {
            const res = await fetch("/api/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            const result = await res.json();

            // Update UI elements
            document.getElementById("predScoreVal").textContent = result.predicted_score;
            document.getElementById("probPassVal").textContent = `${result.pass_probability}%`;
            document.getElementById("probPassBar").style.width = `${result.pass_probability}%`;
            document.getElementById("probFailVal").textContent = `${result.fail_probability}%`;
            document.getElementById("probFailBar").style.width = `${result.fail_probability}%`;
            document.getElementById("predAdviceText").textContent = result.advice;

            const badge = document.getElementById("predResultBadge");
            if (result.result === "PASS") {
                badge.textContent = "PASS";
                badge.className = "px-3 py-1 rounded-full text-xs font-black bg-emerald-500/20 text-emerald-400 border border-emerald-500/40";
            } else {
                badge.textContent = "FAIL";
                badge.className = "px-3 py-1 rounded-full text-xs font-black bg-rose-500/20 text-rose-400 border border-rose-500/40";
            }
        } catch (err) {
            console.error("Error submitting prediction:", err);
        }
    });

    // 4. Student Directory Table & Live Search
    const studentSearchInput = document.getElementById("studentSearchInput");
    const studentsTableBody = document.getElementById("studentsTableBody");
    const studentTableCount = document.getElementById("studentTableCount");

    studentSearchInput.addEventListener("input", e => {
        const query = e.target.value.toLowerCase();
        const filtered = cachedStudents.filter(s =>
            s.name.toLowerCase().includes(query) || s.city.toLowerCase().includes(query)
        );
        renderStudentsTable(filtered);
    });

    function renderStudentsTable(students) {
        studentsTableBody.innerHTML = "";
        studentTableCount.textContent = students.length;

        if (students.length === 0) {
            studentsTableBody.innerHTML = `<tr><td colspan="10" class="px-4 py-8 text-center text-slate-500 font-semibold">No student records found.</td></tr>`;
            return;
        }

        // Limit rendering to 100 rows for DOM performance
        students.slice(0, 100).forEach(s => {
            const tr = document.createElement("tr");
            tr.className = "hover:bg-slate-800/40 transition-colors";

            const badgeClass = s.result === "PASS" ? "badge-pass" : "badge-fail";

            tr.innerHTML = `
                <td class="px-4 py-3 font-mono text-slate-400">#${s.student_id}</td>
                <td class="px-4 py-3 font-bold text-white">${s.name}</td>
                <td class="px-4 py-3 text-slate-300">${s.city}</td>
                <td class="px-4 py-3 text-slate-400">${s.gender}</td>
                <td class="px-4 py-3 text-slate-400">${s.age}</td>
                <td class="px-4 py-3 font-semibold text-cyan-400">${s.attendance}%</td>
                <td class="px-4 py-3 text-slate-300">${s.study_hours}h</td>
                <td class="px-4 py-3 font-bold text-white">${s.final_score}</td>
                <td class="px-4 py-3">
                    <span class="px-2.5 py-1 rounded-full text-[10px] font-black uppercase ${badgeClass}">${s.result}</span>
                </td>
                <td class="px-4 py-3 text-center">
                    <button class="view-radar-btn px-2.5 py-1 bg-brand-600/30 hover:bg-brand-600/50 text-brand-300 border border-brand-500/40 rounded-lg text-xs font-semibold transition-all" data-id="${s.student_id}">
                        <i class="fa-solid fa-chart-radar mr-1"></i> Radar
                    </button>
                </td>
            `;
            studentsTableBody.appendChild(tr);
        });

        // Attach listeners to radar buttons
        document.querySelectorAll(".view-radar-btn").forEach(btn => {
            btn.addEventListener("click", () => {
                const sid = parseInt(btn.getAttribute("data-id"));
                const student = cachedStudents.find(s => s.student_id === sid);
                if (student) openRadarModal(student);
            });
        });
    }

    // 5. Radar Modal Scorecard
    const radarModal = document.getElementById("radarModal");
    const closeModalBtn = document.getElementById("closeModalBtn");

    closeModalBtn.addEventListener("click", () => radarModal.classList.add("hidden"));

    function openRadarModal(s) {
        document.getElementById("modalStudentName").textContent = `${s.name} - Academic Scorecard`;
        document.getElementById("modalStudentDetails").textContent = `${s.city} • ${s.gender}, Age ${s.age} • Result: ${s.result}`;

        radarModal.classList.remove("hidden");

        const ctx = document.getElementById("chartStudentRadar").getContext("2d");
        if (chartRadarInstance) chartRadarInstance.destroy();

        chartRadarInstance = new Chart(ctx, {
            type: "radar",
            data: {
                labels: ["Attendance (%)", "Study Hours (x10)", "Assignments", "Midterm Score", "Previous Score", "Final Score"],
                datasets: [{
                    label: s.name,
                    data: [s.attendance, s.study_hours * 10, s.assignment_score, s.midterm_score, s.previous_score, s.final_score],
                    backgroundColor: "rgba(99, 102, 241, 0.3)",
                    borderColor: "#6366f1",
                    borderWidth: 2,
                    pointBackgroundColor: "#a855f7"
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        angleLines: { color: "#1e293b" },
                        grid: { color: "#1e293b" },
                        pointLabels: { color: "#cbd5e1", font: { family: "Plus Jakarta Sans", size: 11 } },
                        ticks: { color: "#64748b", backdropColor: "transparent" },
                        min: 0,
                        max: 100
                    }
                },
                plugins: { legend: { display: false } }
            }
        });
    }

    // 6. SQL Analytical Insights
    const presetBtns = document.querySelectorAll(".sql-preset-btn");
    const sqlResultTitle = document.getElementById("sqlResultTitle");
    const sqlResultHeader = document.getElementById("sqlResultHeader");
    const sqlResultBody = document.getElementById("sqlResultBody");

    presetBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            presetBtns.forEach(b => b.classList.remove("border-amber-500", "bg-amber-500/10"));
            btn.classList.add("border-amber-500", "bg-amber-500/10");
            const queryType = btn.getAttribute("data-query");
            executeSqlQuery({ query_type: queryType });
        });
    });

    async function executeSqlQuery(payload) {
        try {
            const res = await fetch("/api/sql", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            const data = await res.json();

            if (data.error) {
                alert(data.error);
                return;
            }

            sqlResultTitle.innerHTML = `<i class="fa-solid fa-table text-amber-400"></i> ${data.title} (${data.row_count} records)`;

            // Render Header
            sqlResultHeader.innerHTML = "<tr>" + data.columns.map(c => `<th class="px-4 py-3 font-bold text-slate-300 border-r border-slate-800">${c.replace('_', ' ')}</th>`).join("") + "</tr>";

            // Render Body
            sqlResultBody.innerHTML = "";
            data.rows.forEach(row => {
                const tr = document.createElement("tr");
                tr.className = "hover:bg-slate-800/40 transition-colors border-b border-slate-800/50";
                tr.innerHTML = data.columns.map(c => `<td class="px-4 py-2.5 text-slate-300 border-r border-slate-800/50">${row[c]}</td>`).join("");
                sqlResultBody.appendChild(tr);
            });
        } catch (err) {
            console.error("Error executing SQL query:", err);
        }
    }

    // Auto-load default top_performers query
    executeSqlQuery({ query_type: "top_performers" });

    // Initialize application
    loadMeta();
});
