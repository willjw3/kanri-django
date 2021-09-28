// Pie Chart 
const issue_counts = JSON.parse(document.getElementById('issue_count_data').textContent);
const statuses = Object.keys(issue_counts);
const status_counts = Object.values(issue_counts);

if (statuses.length === 0) {
  let postedIssues = document.getElementById("postedIssues");
  postedIssues.textContent = "No Data To Display";
  postedIssues.classList.add("alert", "alert-danger");
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

const assigned_issue_counts = JSON.parse(document.getElementById('assigned_issue_count_data').textContent);
const assigned_statuses = Object.keys(assigned_issue_counts);
const assigned_status_counts = Object.values(assigned_issue_counts);

if (assigned_statuses.length === 0) {
  let assignedIssues = document.getElementById("assignedIssues");
  assignedIssues.classList.add("alert", "alert-danger");
  assignedIssues.textContent = "No Data To Display";

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


