const $ = id => document.getElementById(id);
const today = new Date();
const isoToday = new Date(today.getTime() - today.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
let view = "overview", timer;
const money = n => new Intl.NumberFormat("en-IN", {style:"currency", currency:"INR", maximumFractionDigits:0}).format(Number(n || 0));
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const initials = s => String(s || "?").split(/\s+/).slice(0, 2).map(x => x[0]).join("").toUpperCase();
const dateText = s => s ? new Date(s + "T00:00:00").toLocaleDateString("en-IN", {day:"numeric", month:"short", year:"numeric"}) : "Not set";

async function api(url, options = {}) {
  let response;
  try {
    response = await fetch(url, options);
  } catch (error) {
    throw new Error("Cannot reach FollowUpPilot. Check that the Terminal server is still running, then refresh this page.");
  }
  const contentType = response.headers.get("content-type") || "";
  let data;
  if (contentType.includes("application/json")) {
    data = await response.json();
  } else {
    const body = await response.text();
    if (response.status === 403) {
      throw new Error("The browser or a security extension blocked this request (403). Try Safari/Chrome, or check Opera VPN, proxy and privacy settings.");
    }
    throw new Error("The server returned an unexpected response. Refresh the page and check the Terminal for errors.");
  }
  if (!response.ok) throw new Error(data.error || "Request failed (" + response.status + ").");
  return data;
}
async function send(url, method, body) {
  return api(url, {method, headers: {"Content-Type":"application/json"}, ...(body ? {body:JSON.stringify(body)} : {})});
}
function toast(message) {
  $("toast").textContent = message;
  $("toast").classList.add("show");
  clearTimeout(timer);
  timer = setTimeout(() => $("toast").classList.remove("show"), 3500);
}
function showLoadError(error) {
  toast(error.message || "Something went wrong.");
  $("rows").innerHTML = '<tr><td colspan="6" class="empty">Could not load leads. Check the server connection and refresh.</td></tr>';
}
async function stats() {
  const s = await api("/api/stats");
  $("total").textContent = s.total;
  $("pipeline").textContent = money(s.pipeline);
  $("due").textContent = s.overdue + s.due_today;
  $("overdue").textContent = s.overdue + " overdue";
  $("conversion").textContent = s.conversion_rate + "%";
  $("converted").textContent = s.converted + " converted leads";
  $("navCount").textContent = s.total;
  const colors = {New:"#aaaebe", Contacted:"#6fa1dc", Interested:"#897ce0", Converted:"#42aa80", Lost:"#df858a"};
  $("stages").innerHTML = ["New","Contacted","Interested","Converted","Lost"].map(k => {
    const n = s.stages[k] || 0;
    return '<div class="stage-row"><span>' + k + '</span><div class="track"><div class="fill" style="width:' + (s.total ? n / s.total * 100 : 0) + '%;background:' + colors[k] + '"></div></div><b>' + n + '</b></div>';
  }).join("");
}
async function load() {
  const params = new URLSearchParams();
  if ($("search").value.trim()) params.set("q", $("search").value.trim());
  if ($("statusFilter").value) params.set("status", $("statusFilter").value);
  const due = $("dueFilter").value || (view === "followups" ? "upcoming" : "");
  if (due) params.set("due", due);
  const list = await api("/api/leads?" + params);
  render(list);
  if (view === "overview") radar(list);
}
function render(list) {
  $("count").textContent = "Showing " + list.length + " leads";
  if (!list.length) {
    $("rows").innerHTML = '<tr><td colspan="6" class="empty">No leads yet. Add your first lead to get started.</td></tr>';
    return;
  }
  $("rows").innerHTML = list.map(l => {
    const late = l.follow_up && l.follow_up < isoToday && !["Converted","Lost"].includes(l.status);
    return '<tr><td><div class="person"><span class="initial">' + esc(initials(l.name)) + '</span><div><strong>' + esc(l.name) + '</strong><small>' + esc(l.company || l.email || "No company") + '</small></div></div></td><td><span class="pill s-' + esc(l.status) + '">' + esc(l.status) + '</span></td><td><b>' + money(l.value) + '</b></td><td class="' + (late ? "overdue" : "") + '">' + (late ? "Overdue · " : "") + dateText(l.follow_up) + '</td><td>' + esc(l.source) + '</td><td><button class="rowbtn" data-edit="' + l.id + '">Edit</button><button class="rowbtn" data-delete="' + l.id + '">×</button></td></tr>';
  }).join("");
}
function radar(list) {
  const horizon = new Date(today.getTime() + 7 * 86400000).toISOString().slice(0, 10);
  const items = list.filter(l => l.follow_up && l.follow_up <= horizon && !["Converted","Lost"].includes(l.status)).slice(0, 4);
  $("radar").innerHTML = items.length ? items.map(l => {
    const late = l.follow_up < isoToday;
    const d = new Date(l.follow_up + "T00:00:00");
    const label = late ? "LATE" : l.follow_up === isoToday ? "TODAY" : d.toLocaleDateString("en-IN", {day:"numeric", month:"short"}).toUpperCase();
    return '<div class="radar"><span class="radar-date ' + (late ? "late" : "") + '">' + label + '</span><div><strong>' + esc(l.name) + '</strong><small>' + esc(l.company || l.status) + ' · ' + money(l.value) + '</small></div></div>';
  }).join("") : '<p class="empty">You’re all caught up. Add a follow-up date to a lead and it will appear here.</p>';
}
function setView(v) {
  view = v;
  document.querySelectorAll(".nav").forEach(b => b.classList.toggle("active", b.dataset.view === v));
  $("crumb").textContent = v === "overview" ? "Overview" : v === "leads" ? "All leads" : "Follow-ups";
  $("title").textContent = v === "overview" ? "Good to see you." : v === "leads" ? "Your leads." : "Follow-up time.";
  $("subtitle").textContent = v === "overview" ? "Here’s what’s happening with your leads today." : v === "leads" ? "Every contact and opportunity, in one place." : "Stay consistent. Keep every opportunity moving.";
  $("overview").style.display = v === "overview" ? "grid" : "none";
  $("tableTitle").textContent = v === "followups" ? "Upcoming follow-ups" : v === "leads" ? "All leads" : "Recent leads";
  $("dueFilter").value = v === "followups" ? "upcoming" : "";
  load().catch(showLoadError);
}
function open(lead) {
  $("form").reset();
  $("leadId").value = lead?.id || "";
  $("modalTitle").textContent = lead ? "Edit lead" : "Add a new lead";
  $("error").textContent = "";
  if (lead) for (const key of ["name","company","email","phone","source","status","value","follow_up","notes"]) $(key).value = lead[key] ?? "";
  else { $("source").value = "Website"; $("status").value = "New"; }
  $("modal").classList.add("open");
}
function close() { $("modal").classList.remove("open"); }

["addTop","addMain"].forEach(id => $(id).onclick = () => open());
$("close").onclick = $("cancel").onclick = close;
$("modal").onclick = event => { if (event.target === $("modal")) close(); };
document.querySelectorAll(".nav").forEach(button => button.onclick = () => setView(button.dataset.view));
document.addEventListener("click", async event => {
  const edit = event.target.closest("[data-edit]");
  const remove = event.target.closest("[data-delete]");
  const go = event.target.closest("[data-goto]");
  try {
    if (edit) open(await api("/api/leads/" + edit.dataset.edit));
    if (remove && confirm("Delete this lead? This cannot be undone.")) {
      await send("/api/leads/" + remove.dataset.delete, "DELETE");
      toast("Lead deleted");
      await refresh();
    }
    if (go) setView(go.dataset.goto);
  } catch (error) { toast(error.message); }
});
$("form").onsubmit = async event => {
  event.preventDefault();
  const keys = ["name","company","email","phone","source","status","value","follow_up","notes"];
  const data = Object.fromEntries(keys.map(key => [key, $(key).value]));
  const id = $("leadId").value;
  try {
    await send(id ? "/api/leads/" + id : "/api/leads", id ? "PATCH" : "POST", data);
    close();
    toast(id ? "Lead updated" : "Lead added");
    await refresh();
  } catch (error) { $("error").textContent = error.message; }
};
["statusFilter","dueFilter"].forEach(id => $(id).onchange = () => load().catch(showLoadError));
$("search").oninput = () => {
  clearTimeout(timer);
  timer = setTimeout(() => load().catch(showLoadError), 250);
};
async function refresh() {
  const results = await Promise.allSettled([stats(), load()]);
  const failed = results.find(result => result.status === "rejected");
  if (failed) throw failed.reason;
}
refresh().catch(showLoadError);
