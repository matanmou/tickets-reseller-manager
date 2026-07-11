const STORAGE_KEY = 'tickets-reseller-data';
const DATA_URL = './data.json';
const appEl = document.getElementById('app');
const flashEl = document.getElementById('flash');
const navLinks = document.querySelectorAll('.main-nav a');

async function fetchInstanceInfo() {
  const badgeEl = document.getElementById('instance-badge');
  if (!badgeEl) {
    return;
  }

  try {
    const tokenRes = await fetch('http://169.254.169.254/latest/api/token', {
      method: 'PUT',
      headers: { 'X-aws-ec2-metadata-token-ttl-seconds': '21600' },
    });

    if (!tokenRes.ok) {
      throw new Error('metadata unavailable');
    }

    const token = await tokenRes.text();
    const [instanceIdRes, privateIpRes, azRes] = await Promise.all([
      fetch('http://169.254.169.254/latest/meta-data/instance-id', {
        headers: { 'X-aws-ec2-metadata-token': token },
      }),
      fetch('http://169.254.169.254/latest/meta-data/local-ipv4', {
        headers: { 'X-aws-ec2-metadata-token': token },
      }),
      fetch('http://169.254.169.254/latest/meta-data/placement/availability-zone', {
        headers: { 'X-aws-ec2-metadata-token': token },
      }),
    ]);

    const instanceId = instanceIdRes.ok ? await instanceIdRes.text() : 'local';
    const privateIp = privateIpRes.ok ? await privateIpRes.text() : null;
    const availabilityZone = azRes.ok ? await azRes.text() : null;

    badgeEl.textContent = `Instance: ${instanceId}`;
    if (privateIp || availabilityZone) {
      badgeEl.title = [privateIp, availabilityZone].filter(Boolean).join(' · ');
    }
  } catch (error) {
    badgeEl.textContent = 'Instance: local';
    badgeEl.title = 'Not running on EC2 metadata';
  }
}

fetchInstanceInfo();

let eventsData = [];
let loaded = false;

function parseDate(value) {
  const [day, month, year] = value.split('/').map(Number);
  return new Date(year, month - 1, day);
}

function formatDate(value) {
  return value;
}

function formatMoney(value) {
  return `${value.toFixed(2)} NIS`;
}

function cloneData(data) {
  return JSON.parse(JSON.stringify(data));
}

function showFlash(message, type = 'success') {
  flashEl.textContent = message;
  flashEl.className = `flash ${type}`;
  flashEl.classList.remove('hidden');
  window.clearTimeout(showFlash._timeout);
  showFlash._timeout = window.setTimeout(() => flashEl.classList.add('hidden'), 4200);
}

function getStoredData() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) {
    return null;
  }
  try {
    return JSON.parse(raw);
  } catch (error) {
    localStorage.removeItem(STORAGE_KEY);
    return null;
  }
}

function saveData() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(eventsData));
}

function getEventByIndex(idx) {
  return eventsData[idx] || null;
}

function sortEvents(events, key) {
  if (key === 'date') {
    return [...events].sort((a, b) => parseDate(a.date) - parseDate(b.date));
  }
  if (key === 'event') {
    return [...events].sort((a, b) => a.event.localeCompare(b.event, 'en', { sensitivity: 'base' }));
  }
  return [...events];
}

function computeTicketStats(event) {
  const soldCount = Object.values(event.sold).reduce((sum, tickets) => sum + tickets.length, 0);
  const availableCount = Object.values(event.available).reduce((sum, tickets) => sum + tickets.length, 0);
  const income = Object.values(event.sold).flat().reduce((sum, ticket) => sum + Number(ticket[3]), 0);
  return { soldCount, availableCount, income };
}

function buildSummary() {
  const today = new Date();
  const thisYear = today.getFullYear();
  const eventsByDate = [...eventsData].sort((a, b) => parseDate(a.date) - parseDate(b.date));

  const upcoming = eventsByDate.filter((event) => parseDate(event.date) >= today);
  const previous = eventsByDate.filter((event) => parseDate(event.date) < today);
  const bySold = eventsData
    .map((event) => ({ event, ...computeTicketStats(event) }))
    .sort((a, b) => b.soldCount - a.soldCount);

  const totalIncome = bySold.reduce((sum, item) => sum + item.income, 0);
  const mostSold = bySold[0] || null;
  const mostIncome = [...bySold].sort((a, b) => b.income - a.income)[0] || null;
  const eventsThisYear = eventsData.filter((event) => parseDate(event.date).getFullYear() === thisYear).length;

  return {
    totalEvents: eventsData.length,
    thisYearLabel: thisYear,
    thisYearCount: eventsThisYear,
    totalIncome,
    mostSoldEvent: mostSold ? mostSold.event.event : null,
    mostSoldCount: mostSold ? mostSold.soldCount : 0,
    mostIncomeEvent: mostIncome ? mostIncome.event.event : null,
    mostIncomeAmount: mostIncome ? mostIncome.income : 0,
    upcomingEvent: upcoming[0] ? upcoming[0].event : null,
    previousEvent: previous.length ? previous[previous.length - 1].event : null,
  };
}

function findTicketBySerial(serial) {
  const search = serial.trim();
  if (!search) return null;
  for (const event of eventsData) {
    for (const [section, tickets] of Object.entries(event.available)) {
      for (const ticket of tickets) {
        if (ticket[0] === search) {
          return { event, section, status: 'Available', ticket };
        }
      }
    }
    for (const [section, tickets] of Object.entries(event.sold)) {
      for (const ticket of tickets) {
        if (ticket[0] === search) {
          return { event, section, status: 'Sold', ticket };
        }
      }
    }
  }
  return null;
}

function getUpcomingEvents() {
  const today = new Date();
  return eventsData.filter((event) => parseDate(event.date) >= today);
}

function getBestSellingEvents() {
  return [...eventsData]
    .map((event) => ({ event, soldCount: computeTicketStats(event).soldCount }))
    .sort((a, b) => b.soldCount - a.soldCount)
    .map((item) => item.event)
    .slice(0, 5);
}

function renderNavigation() {
  const route = location.hash.slice(1).split('?')[0] || '/';
  navLinks.forEach((link) => {
    const target = link.getAttribute('data-route');
    link.classList.toggle('active', target === route);
  });
}

function renderDashboard() {
  const summary = buildSummary();
  const recent = [...eventsData].sort((a, b) => parseDate(b.date) - parseDate(a.date)).slice(0, 8);

  appEl.innerHTML = `
    <section class="actions actions-right">
      <button class="btn btn-secondary" type="button" onclick="navigate('#/events')">Browse all events</button>
      <button class="btn btn-secondary" type="button" onclick="navigate('#/upcoming')">Upcoming only</button>
      <button class="btn btn-secondary" type="button" onclick="navigate('#/summary')">Full summary</button>
      <button class="btn btn-primary" type="button" onclick="navigate('#/new-event')">+ Add event</button>
    </section>
    <div class="grid grid-4">
      <article class="card small-card">
        <div class="card-header">Total events</div>
        <div class="card-body"><strong>${summary.totalEvents}</strong></div>
      </article>
      <article class="card small-card">
        <div class="card-header">Events in ${summary.thisYearLabel}</div>
        <div class="card-body"><strong>${summary.thisYearCount}</strong></div>
      </article>
      <article class="card small-card">
        <div class="card-header">Total income</div>
        <div class="card-body"><strong>${formatMoney(summary.totalIncome)}</strong></div>
      </article>
      <article class="card small-card">
        <div class="card-header">Most tickets sold</div>
        <div class="card-body">
          <strong>${summary.mostSoldEvent || '—'}</strong>
          ${summary.mostSoldEvent ? `<p class="text-muted">${summary.mostSoldCount} sold</p>` : ''}
        </div>
      </article>
    </div>

    <section class="card" style="margin-top: 24px;">
      <div class="card-header">Recent events</div>
      <div class="card-body">
        ${recent.length ? renderEventTable(recent, { showActions: false, title: null }) : '<p class="text-muted">No events yet. Add the first one.</p>'}
      </div>
    </section>
  `;
}

function renderEventTable(events, options = {}) {
  const { showActions = true, title = 'Events', sort = null, showSoldCount = false } = options;
  const headerActions = showActions ? `
    <div class="actions actions-right" style="margin-bottom: 18px;">
      <button class="btn btn-secondary" type="button" onclick="navigate('#/events?sort=date')">Sort by date</button>
      <button class="btn btn-secondary" type="button" onclick="navigate('#/events?sort=event')">Sort by name</button>
      <button class="btn btn-secondary" type="button" onclick="navigate('#/events')">Default</button>
    </div>
  ` : '';

  const rows = events.map((event, index) => {
    const idx = eventsData.indexOf(event);
    const stats = computeTicketStats(event);
    return `
      <tr>
        <td>${idx + 1}</td>
        <td>${event.event}</td>
        <td>${event.date}</td>
        <td>${event.venue}</td>
        ${showSoldCount ? `<td>${stats.soldCount}</td>` : ''}
        <td class="text-right">
          <button class="btn btn-secondary" type="button" onclick="navigate('#/event/${idx}')">Open</button>
          ${showActions ? `<button class="btn btn-secondary" type="button" onclick="navigate('#/event/${idx}/edit')">Edit</button>` : ''}
          ${showActions ? `<button class="btn btn-secondary" type="button" onclick="duplicateEvent(${idx})">Duplicate</button>` : ''}
          ${showActions ? `<button class="btn btn-danger" type="button" onclick="deleteEvent(${idx})">Delete</button>` : ''}
        </td>
      </tr>
    `;
  }).join('');

  return `
    ${headerActions}
    <div class="table-wrapper">
      <table class="table">
        <thead>
          <tr>
            <th>#</th>
            <th>Event</th>
            <th>Date</th>
            <th>Venue</th>
            ${showSoldCount ? '<th>Sold</th>' : ''}
            <th></th>
          </tr>
        </thead>
        <tbody>
          ${rows}
        </tbody>
      </table>
    </div>
  `;
}

function renderEventsList(params) {
  const sort = params.get('sort') || null;
  const view = sort ? sortEvents(eventsData, sort) : [...eventsData];
  appEl.innerHTML = `
    <section class="actions actions-right">
      <button class="btn btn-primary" type="button" onclick="navigate('#/new-event')">+ Add event</button>
    </section>
    <section class="card">
      <div class="card-header">All Events</div>
      <div class="card-body">
        ${view.length ? renderEventTable(view, { sort, showActions: true }) : '<p class="text-muted">No events yet.</p>'}
      </div>
    </section>
  `;
}

function renderEventDetail(idx) {
  const event = getEventByIndex(idx);
  if (!event) {
    appEl.innerHTML = '<p class="text-muted">Event not found.</p>';
    return;
  }
  appEl.innerHTML = `
    <div class="actions actions-right">
      <button class="btn btn-secondary" type="button" onclick="navigate('#/event/${idx}/edit')">Edit info</button>
      <button class="btn btn-primary" type="button" onclick="navigate('#/event/${idx}/add-ticket')">+ Add ticket</button>
    </div>
    <section class="card" style="margin-bottom: 24px;">
      <div class="card-header">${event.event}</div>
      <div class="card-body">
        <p class="text-muted">${event.date} · ${event.venue}</p>
      </div>
    </section>

    <div class="grid" style="grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px;">
      <section class="card">
        <div class="card-header">Available</div>
        <div class="card-body">
          ${renderTicketSection(event.available, true, idx)}
        </div>
      </section>
      <section class="card">
        <div class="card-header">Sold</div>
        <div class="card-body">
          ${renderTicketSection(event.sold, false, idx)}
        </div>
      </section>
    </div>
    <div class="actions" style="margin-top: 24px;">
      <button class="btn btn-secondary" type="button" onclick="navigate('#/events')">← Back to all events</button>
    </div>
  `;
}

function renderTicketSection(bucket, isAvailable, eventIndex) {
  const sections = Object.keys(bucket);
  if (!sections.length) {
    return '<p class="text-muted">No tickets in this section.</p>';
  }
  return sections.map((section) => {
    const rows = bucket[section].map((ticket, pos) => `
      <tr>
        <td>${ticket[0]}</td>
        <td>${ticket[1]}</td>
        <td>${ticket[2]}</td>
        <td>${formatMoney(Number(ticket[3]))}</td>
        <td class="text-right">
          <button class="btn ${isAvailable ? 'btn-primary' : 'btn-secondary'}" type="button" onclick="${isAvailable ? 'sellTicket' : 'unsellTicket'}(${eventIndex}, '${section}', ${pos})">${isAvailable ? 'Sell' : 'Unsell'}</button>
        </td>
      </tr>
    `).join('');
    return `
      <div style="margin-bottom: 18px;">
        <strong>Section ${section}</strong>
        <div class="table-wrapper" style="margin-top: 12px;">
          <table class="table">
            <thead>
              <tr><th>Serial</th><th>Row</th><th>Seat</th><th>Price</th><th></th></tr>
            </thead>
            <tbody>${rows}</tbody>
          </table>
        </div>
      </div>
    `;
  }).join('');
}

function renderEventForm(mode, idx = null) {
  const event = idx !== null ? getEventByIndex(idx) : { event: '', date: '', venue: '' };
  const isNew = mode === 'new';
  appEl.innerHTML = `
    <section class="card form-card">
      <div class="card-header">${isNew ? 'Add Event' : 'Edit Event'}</div>
      <div class="card-body">
        <form id="event-form">
          <div class="form-row two">
            <label>
              Event name
              <input name="event" required value="${event.event || ''}" />
            </label>
            <label>
              Date (DD/MM/YYYY)
              <input name="date" required placeholder="18/01/2026" value="${event.date || ''}" />
            </label>
          </div>
          <div class="form-row">
            <label>
              Venue
              <input name="venue" required value="${event.venue || ''}" />
            </label>
          </div>
          <div class="actions actions-right">
            <button class="btn btn-primary" type="submit">${isNew ? 'Add event' : 'Save changes'}</button>
            <button class="btn btn-secondary" type="button" id="cancel-button">Cancel</button>
          </div>
        </form>
      </div>
    </section>
  `;

  document.getElementById('event-form').addEventListener('submit', (eventSubmit) => {
    eventSubmit.preventDefault();
    const form = eventSubmit.target;
    const name = form.event.value.trim();
    const date = form.date.value.trim();
    const venue = form.venue.value.trim();
    if (!name || !date || !venue) {
      showFlash('Name, date and venue are required.', 'danger');
      return;
    }
    if (isNew) {
      eventsData.push({ event: name, date, venue, available: {}, sold: {} });
      showFlash(`Event '${name}' added.`);
      saveData();
      navigate('#/events');
      return;
    }
    if (!event) {
      showFlash('Event not found.', 'danger');
      return;
    }
    event.event = name;
    event.date = date;
    event.venue = venue;
    saveData();
    showFlash('Event updated.');
    navigate(`#/event/${idx}`);
  });

  document.getElementById('cancel-button').addEventListener('click', () => {
    if (isNew) {
      navigate('#/events');
      return;
    }
    navigate(`#/event/${idx}`);
  });
}

function renderTicketForm(idx) {
  const event = getEventByIndex(idx);
  if (!event) {
    appEl.innerHTML = '<p class="text-muted">Event not found.</p>';
    return;
  }
  appEl.innerHTML = `
    <section class="card form-card">
      <div class="card-header">Add Ticket — ${event.event}</div>
      <div class="card-body">
        <form id="ticket-form">
          <div class="form-row three">
            <label>
              Section
              <input name="section" required />
            </label>
            <label>
              Serial
              <input name="serial" required />
            </label>
            <label>
              Row
              <input name="row" required />
            </label>
          </div>
          <div class="form-row three" style="margin-top: 16px;">
            <label>
              Seat
              <input name="seat" required />
            </label>
            <label>
              Price (NIS)
              <input name="price" required type="number" step="0.01" min="0" />
            </label>
          </div>
          <div class="actions actions-right">
            <button class="btn btn-primary" type="submit">Add ticket</button>
            <button class="btn btn-secondary" type="button" id="cancel-button">Cancel</button>
          </div>
        </form>
      </div>
    </section>
  `;

  document.getElementById('ticket-form').addEventListener('submit', (eventSubmit) => {
    eventSubmit.preventDefault();
    const form = eventSubmit.target;
    const section = form.section.value.trim();
    const serial = form.serial.value.trim();
    const row = form.row.value.trim();
    const seat = form.seat.value.trim();
    const price = Number(form.price.value);
    if (!section || !serial || !row || !seat || Number.isNaN(price)) {
      showFlash('All ticket fields are required and price must be valid.', 'danger');
      return;
    }
    event.available[section] = event.available[section] || [];
    event.available[section].push([serial, row, seat, price]);
    saveData();
    showFlash(`Ticket ${serial} added to section ${section}.`);
    navigate(`# /event/${idx}`.replace(' #', '#'));
  });

  document.getElementById('cancel-button').addEventListener('click', () => navigate(`# /event/${idx}`.replace(' #', '#')));
}

function renderTicketsAvailable() {
  const upcoming = getUpcomingEvents();
  appEl.innerHTML = `
    <section class="card">
      <div class="card-header">Available Tickets (upcoming events)</div>
      <div class="card-body">
        ${upcoming.length ? upcoming.map((event, idx) => renderAvailableCard(event, eventsData.indexOf(event))).join('') : '<p class="text-muted">No upcoming events.</p>'}
      </div>
    </section>
  `;
}

function renderAvailableCard(event, idx) {
  const sections = Object.keys(event.available);
  if (!sections.length) {
    return `
      <section class="card small-card" style="margin-bottom: 16px;">
        <div class="card-body">
          <strong>${event.event}</strong>
          <p class="text-muted">${event.date} · ${event.venue}</p>
          <p class="text-muted">No tickets available for this event.</p>
        </div>
      </section>
    `;
  }
  return `
    <section class="card small-card" style="margin-bottom: 16px;">
      <div class="card-body">
        <div class="actions actions-right" style="margin-bottom: 16px;">
          <button class="btn btn-secondary" type="button" onclick="navigate('#/event/${idx}')">Open</button>
        </div>
        <strong>${event.event}</strong>
        <p class="text-muted">${event.date} · ${event.venue}</p>
        ${sections.map((section) => `
          <div style="margin-top: 14px;">
            <strong>Section ${section}</strong>
            <div class="table-wrapper" style="margin-top: 10px;">
              <table class="table">
                <thead><tr><th>Serial</th><th>Row</th><th>Seat</th><th>Price</th></tr></thead>
                <tbody>
                  ${event.available[section].map((ticket) => `
                    <tr>
                      <td>${ticket[0]}</td>
                      <td>${ticket[1]}</td>
                      <td>${ticket[2]}</td>
                      <td>${formatMoney(Number(ticket[3]))}</td>
                    </tr>
                  `).join('')}
                </tbody>
              </table>
            </div>
          </div>
        `).join('')}
      </div>
    </section>
  `;
}

function renderTicketSearch(params) {
  const serial = params.get('serial') || '';
  const result = serial ? findTicketBySerial(serial) : null;
  const searched = Boolean(serial);
  appEl.innerHTML = `
    <section class="card form-card">
      <div class="card-header">Search Ticket by Serial</div>
      <div class="card-body">
        <form id="search-form">
          <div class="form-row">
            <label>
              Serial number
              <input name="serial" value="${serial}" placeholder="Enter serial number" />
            </label>
          </div>
          <div class="actions actions-right">
            <button class="btn btn-primary" type="submit">Search</button>
          </div>
        </form>
        ${searched ? renderSearchResult(result, serial) : ''}
      </div>
    </section>
  `;

  document.getElementById('search-form').addEventListener('submit', (eventSubmit) => {
    eventSubmit.preventDefault();
    const query = eventSubmit.target.serial.value.trim();
    navigate(`#/search?serial=${encodeURIComponent(query)}`);
  });
}

function renderSearchResult(result, serial) {
  if (!result) {
    return `<p class="text-muted">No ticket with serial "${serial}".</p>`;
  }
  return `
    <section class="card small-card" style="margin-top: 20px;">
      <div class="card-body">
        <h3>Found: ${result.ticket[0]}</h3>
        <dl>
          <dt>Status</dt><dd><span class="badge ${result.status === 'Available' ? 'success' : 'secondary'}">${result.status}</span></dd>
          <dt>Section</dt><dd>${result.section}</dd>
          <dt>Row</dt><dd>${result.ticket[1]}</dd>
          <dt>Seat</dt><dd>${result.ticket[2]}</dd>
          <dt>Price</dt><dd>${formatMoney(Number(result.ticket[3]))}</dd>
          <dt>Event</dt><dd>${result.event.event} · ${result.event.date} · ${result.event.venue}</dd>
        </dl>
      </div>
    </section>
  `;
}

function renderSummary() {
  const summary = buildSummary();
  appEl.innerHTML = `
    <section class="card">
      <div class="card-header">Summary</div>
      <div class="card-body">
        ${eventsData.length === 0 ? '<p class="text-muted">No events yet.</p>' : `
          <div class="grid grid-4">
            <article class="card small-card"><div class="card-header">Total events</div><div class="card-body"><strong>${summary.totalEvents}</strong></div></article>
            <article class="card small-card"><div class="card-header">Events this year</div><div class="card-body"><strong>${summary.thisYearCount}</strong></div></article>
            <article class="card small-card"><div class="card-header">Total income</div><div class="card-body"><strong>${formatMoney(summary.totalIncome)}</strong></div></article>
            <article class="card small-card"><div class="card-header">Top selling event</div><div class="card-body"><strong>${summary.mostSoldEvent || '—'}</strong><p class="text-muted">${summary.mostSoldCount} sold</p></div></article>
            <article class="card small-card"><div class="card-header">Top income event</div><div class="card-body"><strong>${summary.mostIncomeEvent || '—'}</strong><p class="text-muted">${summary.mostIncomeAmount ? formatMoney(summary.mostIncomeAmount) : ''}</p></div></article>
            <article class="card small-card"><div class="card-header">Upcoming event</div><div class="card-body"><strong>${summary.upcomingEvent || 'None'}</strong></div></article>
            <article class="card small-card"><div class="card-header">Previous event</div><div class="card-body"><strong>${summary.previousEvent || 'None'}</strong></div></article>
          </div>
        `}
      </div>
    </section>
  `;
}

function renderNotFound() {
  appEl.innerHTML = '<p class="text-muted">Page not found.</p>';
}

function navigate(hash) {
  window.location.hash = hash;
}

function duplicateEvent(idx) {
  const event = getEventByIndex(idx);
  if (!event) return showFlash('Event not found.', 'danger');
  const clone = {
    event: event.event,
    date: event.date,
    venue: event.venue,
    available: {},
    sold: {},
  };
  eventsData.push(clone);
  saveData();
  showFlash(`Event '${event.event}' duplicated.`);
  renderRoute();
}

function deleteEvent(idx) {
  const event = getEventByIndex(idx);
  if (!event) return showFlash('Event not found.', 'danger');
  if (!window.confirm(`Delete event '${event.event}'?`)) {
    return;
  }
  eventsData.splice(idx, 1);
  saveData();
  showFlash(`Event '${event.event}' deleted.`);
  renderRoute();
}

function sellTicket(eventIdx, section, pos) {
  const event = getEventByIndex(eventIdx);
  if (!event) return showFlash('Event not found.', 'danger');
  const bucket = event.available[section] || [];
  if (pos < 0 || pos >= bucket.length) return showFlash('Ticket not found.', 'danger');
  const ticket = bucket.splice(pos, 1)[0];
  if (bucket.length === 0) delete event.available[section];
  event.sold[section] = event.sold[section] || [];
  event.sold[section].push(ticket);
  saveData();
  showFlash(`Ticket ${ticket[0]} sold.`);
  renderRoute();
}

function unsellTicket(eventIdx, section, pos) {
  const event = getEventByIndex(eventIdx);
  if (!event) return showFlash('Event not found.', 'danger');
  const bucket = event.sold[section] || [];
  if (pos < 0 || pos >= bucket.length) return showFlash('Ticket not found.', 'danger');
  const ticket = bucket.splice(pos, 1)[0];
  if (bucket.length === 0) delete event.sold[section];
  event.available[section] = event.available[section] || [];
  event.available[section].push(ticket);
  saveData();
  showFlash(`Ticket ${ticket[0]} marked unsold.`);
  renderRoute();
}

function loadInitialData() {
  const stored = getStoredData();
  if (stored) {
    eventsData = stored;
    loaded = true;
    renderRoute();
    return;
  }
  fetch(DATA_URL)
    .then((response) => response.json())
    .then((data) => {
      eventsData = data;
      saveData();
      loaded = true;
      renderRoute();
    })
    .catch(() => {
      showFlash('Unable to load sample data. Please run a static server next to frontend/data.json.', 'warning');
      eventsData = [];
      loaded = true;
      renderRoute();
    });
}

function renderRoute() {
  renderNavigation();
  const raw = location.hash.slice(1) || '/';
  const [pathPart, query = ''] = raw.split('?');
  const segments = pathPart.split('/').filter(Boolean);
  const params = new URLSearchParams(query);

  if (!loaded) {
    appEl.innerHTML = '<p class="text-muted">Loading…</p>';
    return;
  }

  if (segments.length === 0) {
    renderDashboard();
    return;
  }

  if (segments[0] === 'events') {
    renderEventsList(params);
    return;
  }

  if (segments[0] === 'upcoming') {
    const upcoming = getUpcomingEvents();
    appEl.innerHTML = `
      <section class="card">
        <div class="card-header">Upcoming Events</div>
        <div class="card-body">
          ${upcoming.length ? renderEventTable(upcoming, { showActions: true }) : '<p class="text-muted">No upcoming events.</p>'}
        </div>
      </section>
    `;
    return;
  }

  if (segments[0] === 'best-selling') {
    const best = getBestSellingEvents();
    appEl.innerHTML = `
      <section class="card">
        <div class="card-header">Top 5 Best-Selling Events</div>
        <div class="card-body">
          ${best.length ? renderEventTable(best, { showActions: false, showSoldCount: true }) : '<p class="text-muted">No sales yet.</p>'}
        </div>
      </section>
    `;
    return;
  }

  if (segments[0] === 'available') {
    renderTicketsAvailable();
    return;
  }

  if (segments[0] === 'search') {
    renderTicketSearch(params);
    return;
  }

  if (segments[0] === 'summary') {
    renderSummary();
    return;
  }

  if (segments[0] === 'new-event') {
    renderEventForm('new');
    return;
  }

  if (segments[0] === 'event') {
    const idx = Number(segments[1]);
    if (Number.isNaN(idx)) {
      renderNotFound();
      return;
    }
    if (segments[2] === 'edit') {
      renderEventForm('edit', idx);
      return;
    }
    if (segments[2] === 'add-ticket') {
      renderTicketForm(idx);
      return;
    }
    renderEventDetail(idx);
    return;
  }

  renderNotFound();
}

window.addEventListener('hashchange', renderRoute);
window.navigate = navigate;
window.duplicateEvent = duplicateEvent;
window.deleteEvent = deleteEvent;
window.sellTicket = sellTicket;
window.unsellTicket = unsellTicket;

loadInitialData();
