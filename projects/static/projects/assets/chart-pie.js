// Pie Chart 
const task_counts = JSON.parse(document.getElementById('task_count_data').textContent);
const statuses = Object.keys(task_counts);
const status_counts = Object.values(task_counts);

if (statuses.length === 0) {
  let postedTasks = document.getElementById("postedTasks");
  postedTasks.textContent = "No Data To Display";
  postedTasks.classList.add("alert", "alert-danger");
} else {
  var ctx = document.getElementById("postedIssuePie");
  var myPieChart = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: statuses,
      datasets: [{
        data: status_counts,
        backgroundColor: ['#007bff', '#dc3545', '#ffc107', '#28a745'],
      }],
    },
  });
}

const assigned_task_counts = JSON.parse(document.getElementById('assigned_task_count_data').textContent);
const assigned_statuses = Object.keys(assigned_task_counts);
const assigned_status_counts = Object.values(assigned_task_counts);

if (assigned_statuses.length === 0) {
  let assignedTasks = document.getElementById("assignedTasks");
  assignedTasks.classList.add("alert", "alert-danger");
  assignedTasks.textContent = "No Data To Display";

} else {
  var ctx_assigned = document.getElementById("assignedIssuePie");
  var myAssignedPieChart = new Chart(ctx_assigned, {
    type: 'pie',
    data: {
      labels: assigned_statuses,
      datasets: [{
        data: assigned_status_counts,
        backgroundColor: ['#007bff', '#dc3545', '#ffc107', '#28a745'],
      }],
    },
  });
}


