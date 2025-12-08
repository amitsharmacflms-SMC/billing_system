const API_BASE = "https://billingsystem-production.up.railway.app";
const token = localStorage.getItem("token");

function goMenu(){ window.location.href = "/menu"; }
async function loadUsers(){
  const res = await fetch(`${API_BASE}/users/`, { headers:{ Authorization:`Bearer ${token}` }});
  const list = await res.json();
  const body = document.getElementById('userTableBody');
  body.innerHTML = "";
  list.forEach(u=>{
    body.innerHTML += `<tr>
      <td><input id="n${u.id}" value="${u.name}"></td>
      <td><input id="e${u.id}" value="${u.email}"></td>
      <td><input id="s${u.id}" value="${u.state||''}"></td>
      <td>
        <select id="r${u.id}">
          <option ${u.role=='admin'?'selected':''}>admin</option>
          <option ${u.role=='supplier'?'selected':''}>supplier</option>
          <option ${u.role=='user'?'selected':''}>user</option>
        </select>
      </td>
      <td><input id="sp${u.id}" value="${u.supplier_id||''}"></td>
      <td><select id="a${u.id}"><option value="true" ${u.active?'selected':''}>Active</option><option value="false" ${!u.active?'selected':''}>Inactive</option></select></td>
      <td>
        <button onclick="updateUser(${u.id})">Save</button>
        <button onclick="resetPass(${u.id})">Reset</button>
        <button onclick="deleteUser(${u.id})">Delete</button>
      </td>
    </tr>`;
  });
}

async function updateUser(id){
  const payload = {
    name: document.getElementById(`n${id}`).value,
    email: document.getElementById(`e${id}`).value,
    state: document.getElementById(`s${id}`).value,
    role: document.getElementById(`r${id}`).value,
    supplier_id: document.getElementById(`sp${id}`).value || null,
    active: document.getElementById(`a${id}`).value === "true"
  };
  await fetch(`${API_BASE}/users/update/${id}`, {
    method:'PUT', headers:{ 'Content-Type':'application/json', Authorization:`Bearer ${token}`}, body:JSON.stringify(payload)
  });
  alert('Updated');
  loadUsers();
}

async function deleteUser(id){
  if(!confirm('Delete?')) return;
  await fetch(`${API_BASE}/users/delete/${id}`, { method:'DELETE', headers:{ Authorization:`Bearer ${token}` } });
  loadUsers();
}

async function resetPass(id){
  const pass = prompt('New password:');
  if(!pass) return;
  await fetch(`${API_BASE}/users/reset-password/${id}`, { method:'PUT', headers:{ 'Content-Type':'application/json', Authorization:`Bearer ${token}`}, body:JSON.stringify({ password: pass })});
  alert('Password reset');
}

function openAddUser(){
  window.location.href = '/add-user';
}

window.onload = loadUsers;
