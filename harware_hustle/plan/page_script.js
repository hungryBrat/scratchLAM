(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var fx = function (x, d) { return (x == null || !isFinite(x)) ? '–' : Number(x).toFixed(d == null ? 3 : d); };
  var esc = function (s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };

  function toast(msg) {
    var t = $('#toast');
    t.textContent = msg;
    t.classList.add('on');
    clearTimeout(toast.timer);
    toast.timer = setTimeout(function () { t.classList.remove('on'); }, 1800);
  }
  function local(key, val) {
    try {
      if (val === undefined) { var v = localStorage.getItem(key); return v ? JSON.parse(v) : null; }
      localStorage.setItem(key, JSON.stringify(val));
    } catch (e) { return null; }
    return null;
  }
  function num(id) { var v = parseFloat($(id).value); return isFinite(v) ? v : NaN; }

  /* countdown to Sun 4 Oct 2026 18:00 IST */
  var CUTOFF = Date.UTC(2026, 9, 4, 12, 30, 0);
  function tick() {
    var c = $('#countdown');
    var ms = CUTOFF - Date.now();
    if (ms <= 0) { c.textContent = 'cutoff passed'; return; }
    var d = Math.floor(ms / 864e5), h = Math.floor(ms % 864e5 / 36e5), m = Math.floor(ms % 36e5 / 6e4);
    c.textContent = d + ' d ' + h + ' h ' + m + ' min';
  }
  tick();
  setInterval(tick, 20000);

  /* copy buttons */
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-copy-from]');
    if (!b) return;
    var src = $(b.dataset.copyFrom);
    var text = src ? src.textContent : '';
    var fallback = function () {
      var r = document.createRange(); r.selectNodeContents(src);
      var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
      toast('Selected. Press Ctrl+C to copy.');
    };
    try { navigator.clipboard.writeText(text).then(function () { toast('Copied'); }, fallback); } catch (err) { fallback(); }
  });

  /* statistics */
  var T975 = [NaN, 12.706, 4.303, 3.182, 2.776, 2.571, 2.447, 2.365, 2.306, 2.262, 2.228, 2.201, 2.179, 2.160, 2.145, 2.131, 2.120, 2.110, 2.101, 2.093, 2.086];
  function t975(dof) { return dof <= 0 ? NaN : (dof < T975.length ? T975[dof] : 1.96 + 2.4 / dof); }
  function linfit(xs, ys) {
    var n = xs.length, xm = 0, ym = 0, sxx = 0, sxy = 0, syy = 0, ssr = 0, i;
    for (i = 0; i < n; i++) { xm += xs[i]; ym += ys[i]; }
    xm /= n; ym /= n;
    for (i = 0; i < n; i++) { sxx += (xs[i] - xm) * (xs[i] - xm); sxy += (xs[i] - xm) * (ys[i] - ym); syy += (ys[i] - ym) * (ys[i] - ym); }
    var a = sxy / sxx, b = ym - a * xm;
    for (i = 0; i < n; i++) ssr += Math.pow(ys[i] - (a * xs[i] + b), 2);
    var s = n > 2 ? Math.sqrt(ssr / (n - 2)) : NaN;
    return { a: a, b: b, xm: xm, sxx: sxx, n: n, s: s, r2: syy > 0 ? 1 - ssr / syy : NaN, seA: s / Math.sqrt(sxx), seB: s * Math.sqrt(1 / n + xm * xm / sxx) };
  }

  /* small SVG chart */
  function ticks(lo, hi, n) {
    var span = (hi - lo) || 1, raw = span / (n || 5), mag = Math.pow(10, Math.floor(Math.log10(raw))), e = raw / mag;
    var step = (e >= 7.5 ? 10 : e >= 3.5 ? 5 : e >= 1.5 ? 2 : 1) * mag, out = [];
    for (var v = Math.ceil(lo / step) * step; v <= hi + step * 1e-6; v += step) out.push(+v.toFixed(10));
    return out;
  }
  function drawChart(svg, o) {
    var W = 560, H = 330, L = 58, R = 14, T = 14, B = 46, pw = W - L - R, ph = H - T - B;
    var X = function (v) { return L + (v - o.xlo) / (o.xhi - o.xlo) * pw; };
    var Y = function (v) { return T + ph - (v - o.ylo) / (o.yhi - o.ylo) * ph; };
    var clip = function (v) { return Math.max(o.ylo, Math.min(o.yhi, v)); };
    var g = '';
    if (o.hband) g += '<rect class="okband" x="' + L + '" y="' + Y(o.hband[1]) + '" width="' + pw + '" height="' + (Y(o.hband[0]) - Y(o.hband[1])) + '"/>';
    ticks(o.xlo, o.xhi).forEach(function (t) {
      g += '<line class="grid" x1="' + X(t) + '" x2="' + X(t) + '" y1="' + T + '" y2="' + (T + ph) + '"/><text x="' + X(t) + '" y="' + (T + ph + 16) + '" text-anchor="middle">' + (+t.toPrecision(6)) + '</text>';
    });
    ticks(o.ylo, o.yhi).forEach(function (t) {
      g += '<line class="grid" x1="' + L + '" x2="' + (L + pw) + '" y1="' + Y(t) + '" y2="' + Y(t) + '"/><text x="' + (L - 6) + '" y="' + (Y(t) + 4) + '" text-anchor="end">' + (+t.toPrecision(6)) + '</text>';
    });
    if (o.zero) g += '<line class="zero" x1="' + L + '" x2="' + (L + pw) + '" y1="' + Y(0) + '" y2="' + Y(0) + '"/>';
    (o.bands || []).forEach(function (b) {
      var top = b.map(function (p) { return X(p[0]) + ',' + Y(clip(p[2])); }).join(' ');
      var bot = b.slice().reverse().map(function (p) { return X(p[0]) + ',' + Y(clip(p[1])); }).join(' ');
      g += '<polygon class="band" points="' + top + ' ' + bot + '"/>';
    });
    (o.lines || []).forEach(function (ln) {
      g += '<polyline class="' + ln.cls + '" points="' + ln.pts.map(function (p) { return X(p[0]) + ',' + Y(clip(p[1])); }).join(' ') + '"/>';
    });
    o.xs.forEach(function (x, i) { g += '<circle class="pt" cx="' + X(x) + '" cy="' + Y(clip(o.ys[i])) + '" r="4.5"/>'; });
    g += '<line class="axis" x1="' + L + '" x2="' + (L + pw) + '" y1="' + (T + ph) + '" y2="' + (T + ph) + '"/><line class="axis" x1="' + L + '" x2="' + L + '" y1="' + T + '" y2="' + (T + ph) + '"/>';
    g += '<text x="' + (L + pw / 2) + '" y="' + (H - 8) + '" text-anchor="middle">' + o.xlab + '</text>';
    g += '<text x="14" y="' + (T + ph / 2) + '" text-anchor="middle" transform="rotate(-90 14 ' + (T + ph / 2) + ')">' + o.ylab + '</text>';
    svg.innerHTML = g;
  }

  /* ---------------- capabilities ---------------- */
  var caps = { db: null, user: null, downloads: null, uid: null };
  var ready = (window.claude && window.claude.use) ? Promise.all([
    window.claude.use('db').catch(function () { return null; }),
    window.claude.use('user').catch(function () { return null; }),
    window.claude.use('downloads').catch(function () { return null; })
  ]) : Promise.resolve([null, null, null]);

  async function names(ids) {
    if (!caps.user || !ids.length) return {};
    try { return await caps.user.profiles(ids); } catch (e) { return {}; }
  }
  function hhmm(ms) { var d = new Date(ms); return ('0' + d.getHours()).slice(-2) + ':' + ('0' + d.getMinutes()).slice(-2); }

  /* ---------------- calibration workbench ---------------- */
  var EXAMPLE = [[8329, 90, 1500], [8352, 90, 1501], [8333, 90, 1498], [11115, 60, 1989], [11170, 60, 2000], [11091, 60, 1983],
    [16708, 60, 2981], [16832, 60, 3002], [16667, 60, 2973], [16678, 45, 2988], [16693, 45, 2984], [16846, 45, 3008],
    [17883, 40, 3200], [18042, 40, 3219], [18031, 40, 3217]].map(function (r, i) { return { id: 'ex' + i, pulses: r[0], time_s: r[1], mass_g: r[2], example: true }; });
  var cal = { runs: [], mode: 'local', del: null };

  function calData() {
    var rho = num('#cal-rho') || 1000;
    var rows = (cal.runs.length ? cal.runs : EXAMPLE).map(function (r) {
      var o = Object.assign({}, r);
      o.f = r.pulses / r.time_s;
      if (r.mass_g > 0) { o.V = r.mass_g / rho; o.Q = o.V / r.time_s * 60; o.K = r.pulses / o.V; }
      return o;
    });
    var good = rows.filter(function (r) { return r.Q > 0; });
    var fit = good.length >= 2 ? linfit(good.map(function (r) { return r.f; }), good.map(function (r) { return r.Q; })) : null;
    if (fit) rows.forEach(function (r) { if (r.Q > 0) { r.Qf = fit.a * r.f + fit.b; r.err = (r.Qf - r.Q) / r.Q * 100; } });
    return { rows: rows, good: good, fit: fit, example: !cal.runs.length };
  }

  function renderCal() {
    var d = calData();
    $('#cal-example').hidden = !d.example;
    var tb = $('#cal-rows');
    tb.innerHTML = '';
    d.rows.forEach(function (r, i) {
      var tr = document.createElement('tr');
      var massCell = r.example ? fx(r.mass_g, 0)
        : '<input type="number" class="narrow" step="1" min="0" aria-label="Net mass, run ' + (i + 1) + '" data-mass="' + esc(r.id) + '" value="' + (r.mass_g > 0 ? r.mass_g : '') + '">';
      var act = r.example ? '' : (cal.del === r.id
        ? '<button class="ghost" data-delok="' + esc(r.id) + '" type="button">Confirm delete</button>'
        : '<button class="ghost" data-del="' + esc(r.id) + '" type="button">Delete</button>');
      tr.innerHTML = '<td>' + (i + 1) + (r.note ? ' <span class="muted small">' + esc(r.note) + '</span>' : '') + '</td>' +
        '<td class="num">' + fx(r.pulses, 0) + '</td><td class="num">' + fx(r.time_s, 3) + '</td><td class="num">' + fx(r.f, 2) + '</td>' +
        '<td class="num">' + massCell + '</td><td class="num">' + fx(r.V, 4) + '</td><td class="num">' + fx(r.Q, 3) + '</td>' +
        '<td class="num">' + fx(r.Qf, 3) + '</td><td class="num">' + (r.err == null ? '–' : (r.err >= 0 ? '+' : '') + fx(r.err, 2)) + '</td>' +
        '<td class="num">' + fx(r.K, 0) + '</td><td>' + act + '</td>';
      tb.appendChild(tr);
    });
    if (!d.rows.length) tb.innerHTML = '<tr><td colspan="11" class="muted">No runs yet. Run CAL on the console, then add pulses, time and the weighed mass here.</td></tr>';

    var out = $('#cal-out'), f = d.fit;
    if (!f || d.good.length < 3) {
      out.innerHTML = '<div class="kv"><div class="k">Status</div><div class="v"><small>Need three or more weighed runs</small></div></div>';
      $('#cal-cmds').textContent = 'Add three or more weighed runs to get the SET commands.';
      $('#cal-chart').innerHTML = '';
      $('#cal-resid').innerHTML = '';
      return;
    }
    var errs = d.good.map(function (r) { return Math.abs(r.err); });
    var Ks = d.good.map(function (r) { return r.K; });
    var Km = Ks.reduce(function (a, b) { return a + b; }, 0) / Ks.length;
    var Ksd = Math.sqrt(Ks.reduce(function (a, b) { return a + (b - Km) * (b - Km); }, 0) / Math.max(1, Ks.length - 1));
    var f3 = (3 - f.b) / f.a;
    var pi = t975(f.n - 2) * f.s * Math.sqrt(1 + 1 / f.n + Math.pow(f3 - f.xm, 2) / f.sxx);
    var maxE = Math.max.apply(null, errs), avgE = errs.reduce(function (a, b) { return a + b; }, 0) / errs.length;
    var groups = {};
    d.good.forEach(function (r) { if (r.duty) (groups[r.duty] = groups[r.duty] || []).push(r.K); });
    var rep = null;
    Object.keys(groups).forEach(function (k) {
      var g = groups[k];
      if (g.length < 2) return;
      var m = g.reduce(function (a, b) { return a + b; }, 0) / g.length, half = (Math.max.apply(null, g) - Math.min.apply(null, g)) / 2 / m * 100;
      rep = rep == null ? half : Math.max(rep, half);
    });
    var pass = maxE <= 3 && (rep == null || rep <= 1);
    var kv = function (k, v, small) { return '<div class="kv"><div class="k">' + k + '</div><div class="v">' + v + (small ? ' <small>' + small + '</small>' : '') + '</div></div>'; };
    out.innerHTML =
      kv('Max error', fx(maxE, 2) + ' %', pass ? '<span class="pill ok">meets M3</span>' : '<span class="pill warn">below target</span>') +
      kv('Repeatability', rep == null ? '–' : '± ' + fx(rep, 2) + ' %', rep == null ? 'enter the duty on each run' : 'worst flow; M3 needs ± 1%') +
      kv('R²', fx(f.r2, 5), 'reported, not the gate') +
      kv('a (L/min per Hz)', fx(f.a, 6), '± ' + fx(f.seA, 6)) +
      kv('b (L/min)', (f.b >= 0 ? '+' : '') + fx(f.b, 4), '± ' + fx(f.seB, 4)) +
      kv('Average error', fx(avgE, 2) + ' %') +
      kv('K (pulses/L)', fx(Km, 0), '± ' + fx(Ksd, 0) + ' · ' + (Km / 5880 * 100 - 100 >= 0 ? '+' : '') + fx(Km / 5880 * 100 - 100, 1) + '% vs 5880') +
      kv('At 3.00 L/min', '± ' + fx(pi, 3), 'L/min, 95% PI') +
      kv('Runs used', d.good.length + '', d.example ? 'example data' : '');
    var fcut = Math.max(3, 0.8 * (0.3 - f.b) / f.a);
    $('#cal-cmds').textContent = d.example
      ? 'Example data: no commands until your own runs are in.'
      : 'SET a ' + f.a.toFixed(6) + '\nSET b ' + f.b.toFixed(5) + '\nSET fcut ' + fcut.toFixed(1) + '\nSAVE';

    var xs = d.good.map(function (r) { return r.f; }), ys = d.good.map(function (r) { return r.Q; });
    var xhi = Math.max.apply(null, xs) * 1.08, yhi = Math.max.apply(null, ys) * 1.12;
    var line = [], band = [], dsl = [];
    for (var k = 0; k <= 40; k++) {
      var x = xhi * k / 40, yv = f.a * x + f.b, w = t975(f.n - 2) * f.s * Math.sqrt(1 + 1 / f.n + Math.pow(x - f.xm, 2) / f.sxx);
      line.push([x, yv]); band.push([x, yv - w, yv + w]); dsl.push([x, x / 98]);
    }
    drawChart($('#cal-chart'), { xs: xs, ys: ys, xlo: 0, xhi: xhi, ylo: 0, yhi: yhi, xlab: 'FT-01 frequency f (Hz)', ylab: 'actual flow Q (L/min)', lines: [{ cls: 'ds', pts: dsl }, { cls: 'fit', pts: line }], bands: [band] });
    var es = d.good.map(function (r) { return r.err; });
    var emax = Math.max(2.5, Math.max.apply(null, es.map(Math.abs)) * 1.2);
    drawChart($('#cal-resid'), { xs: ys, ys: es, xlo: 0, xhi: yhi, ylo: -emax, yhi: emax, xlab: 'actual flow Q (L/min)', ylab: 'fit error (%)', hband: [-2, 2], zero: true, lines: [] });
  }

  function saveLocalRuns() { if (cal.mode === 'local') local('hh-cal-runs', cal.runs); }
  async function addRun(r) {
    r.at = Date.now();
    if (caps.uid) r.by = caps.uid;
    if (cal.mode === 'db') {
      try { await caps.db.collection('cal_runs').add(r); } catch (e) { toast('Could not save the run: ' + (e && e.code || 'error')); }
    } else {
      r.id = 'l' + r.at + Math.floor(Math.random() * 1e4);
      cal.runs.push(r); saveLocalRuns(); renderCal();
    }
  }
  $('#cal-add').addEventListener('click', function () {
    var p = num('#cal-pulses'), t = num('#cal-time');
    if (!(p > 0 && t > 0)) { toast('Enter pulses and time first'); return; }
    var m = num('#cal-mass');
    var r = { pulses: p, time_s: t, mass_g: m > 0 ? m : null, duty: num('#cal-duty') || null, note: $('#cal-note').value.trim().slice(0, 40) };
    addRun(r).then(function () { ['#cal-pulses', '#cal-time', '#cal-mass', '#cal-note'].forEach(function (s) { $(s).value = ''; }); });
  });
  $('#cal-paste-go').addEventListener('click', async function () {
    var lines = $('#cal-paste').value.split(/\r?\n/), n = 0;
    for (var i = 0; i < lines.length; i++) {
      var p = lines[i].trim().split(',');
      if (p[0] !== 'C' || p.length < 7) continue;
      var pulses = parseFloat(p[3]), t = parseFloat(p[4]);
      if (pulses > 0 && t > 0) { await addRun({ pulses: pulses, time_s: t, mass_g: null, duty: Math.round(parseFloat(p[6]) * 100) || null, note: 'run ' + p[2] }); n++; }
    }
    $('#cal-paste').value = '';
    toast(n ? n + ' run(s) added. Enter each mass when weighed.' : 'No C,… lines found');
  });
  $('#cal-rows').addEventListener('change', async function (e) {
    var id = e.target.dataset.mass;
    if (!id) return;
    var m = parseFloat(e.target.value);
    var val = m > 0 ? m : null;
    if (cal.mode === 'db') {
      try { await caps.db.collection('cal_runs').doc(id).update({ mass_g: val }); } catch (err) { toast('Could not save the mass'); }
    } else {
      cal.runs.forEach(function (r) { if (r.id === id) r.mass_g = val; }); saveLocalRuns(); renderCal();
    }
  });
  $('#cal-rows').addEventListener('click', async function (e) {
    var b = e.target.closest('button');
    if (!b) return;
    if (b.dataset.del) { cal.del = b.dataset.del; renderCal(); return; }
    if (b.dataset.delok) {
      var id = b.dataset.delok; cal.del = null;
      if (cal.mode === 'db') { try { await caps.db.collection('cal_runs').doc(id).delete(); } catch (err) { toast('Could not delete'); } }
      else { cal.runs = cal.runs.filter(function (r) { return r.id !== id; }); saveLocalRuns(); renderCal(); }
    }
  });
  $('#cal-rho').addEventListener('input', renderCal);
  $('#cal-csv').addEventListener('click', async function () {
    var d = calData();
    if (d.example) { toast('Nothing to export yet'); return; }
    var csv = 'run,pulses,time_s,f_hz,mass_g,volume_l,q_actual_lpm,q_fit_lpm,error_pct,k_pulses_per_l,duty_pct,note\n' + d.rows.map(function (r, i) {
      return [i + 1, r.pulses, r.time_s, fx(r.f, 3), r.mass_g || '', r.V ? r.V.toFixed(4) : '', r.Q ? r.Q.toFixed(4) : '', r.Qf ? r.Qf.toFixed(4) : '', r.err != null ? r.err.toFixed(3) : '', r.K ? r.K.toFixed(1) : '', r.duty || '', '"' + String(r.note || '').replace(/"/g, "'") + '"'].join(',');
    }).join('\n') + '\n';
    if (!caps.downloads) { $('#cal-csv-note').textContent = 'Downloads are not available in this view.'; return; }
    try { await caps.downloads.save({ filename: 'ft01_calibration_runs.csv', data: csv }); toast('Saved'); }
    catch (err) { if (err && err.code !== 'declined') $('#cal-csv-note').textContent = 'Could not save the file (' + (err.code || 'error') + ').'; }
  });

  /* ---------------- checklists ---------------- */
  var CHECKS = {{CHECKS}};
  var chk = { state: {}, mode: 'local' };
  function renderChecks() {
    var host = $('#checks');
    var ids = [];
    Object.keys(chk.state).forEach(function (k) { if (chk.state[k] && chk.state[k].by) ids.push(chk.state[k].by); });
    names(Array.from(new Set(ids))).then(function (ps) {
      host.innerHTML = '';
      CHECKS.forEach(function (g) {
        var done = g.items.filter(function (it) { return chk.state[it[0]] && chk.state[it[0]].done; }).length;
        var sec = document.createElement('div');
        sec.className = 'cgroup';
        var html = '<header><h3>' + g.title + '</h3><span class="mono small">' + done + '/' + g.items.length + '</span></header><div class="bar"><i style="width:' + (done / g.items.length * 100) + '%"></i></div>';
        g.items.forEach(function (it) {
          var s = chk.state[it[0]] || {};
          var who = '';
          if (s.done) {
            var nm = s.by && ps[s.by] ? (ps[s.by].name || 'Someone') : (chk.mode === 'local' ? 'you' : 'Someone');
            who = '<span class="who">' + esc(nm) + (s.at ? ' · ' + hhmm(s.at) : '') + '</span>';
          }
          html += '<div class="citem' + (s.done ? ' done' : '') + '"><input type="checkbox" id="c-' + it[0] + '" data-chk="' + it[0] + '"' + (s.done ? ' checked' : '') + '><label for="c-' + it[0] + '">' + it[1] + '</label>' + who + '</div>';
        });
        sec.innerHTML = html;
        host.appendChild(sec);
      });
      document.querySelectorAll('#team [data-chk]').forEach(function (box) {
        var s = chk.state[box.dataset.chk] || {};
        var row = box.closest('.citem');
        box.checked = !!s.done;
        row.classList.toggle('done', !!s.done);
        var nm = s.by && ps[s.by] ? (ps[s.by].name || 'Someone') : (chk.mode === 'local' ? 'you' : 'Someone');
        row.querySelector('.who').textContent = s.done ? nm + (s.at ? ' · ' + hhmm(s.at) : '') : '';
      });
    });
  }
  async function onTick(e) {
    var id = e.target.dataset.chk;
    if (!id) return;
    var rec = { done: e.target.checked, at: Date.now() };
    if (caps.uid) rec.by = caps.uid;
    if (chk.mode === 'db') {
      try { await caps.db.collection('checks').doc(id).set(rec); }
      catch (err) { e.target.checked = !e.target.checked; toast('Could not save the tick'); }
    } else {
      chk.state[id] = rec; local('hh-checks', chk.state); renderChecks();
    }
  }
  $('#checks').addEventListener('change', onTick);
  $('#team').addEventListener('change', onTick);

  /* ---------------- role names and the bench log ---------------- */
  var shared = { team: {}, bench: {}, mode: 'local' };
  function renderShared() {
    document.querySelectorAll('[data-role]').forEach(function (inp) {
      var d = shared.team[inp.dataset.role];
      if (document.activeElement !== inp) inp.value = d && d.name ? d.name : '';
    });
    var ids = [];
    Object.keys(shared.bench).forEach(function (k) { if (shared.bench[k] && shared.bench[k].by) ids.push(shared.bench[k].by); });
    names(Array.from(new Set(ids))).then(function (ps) {
      document.querySelectorAll('[data-bench]').forEach(function (inp) {
        var d = shared.bench[inp.dataset.bench];
        if (document.activeElement !== inp) inp.value = d && d.value ? d.value : '';
        var who = (d && d.value) ? ((d.by && ps[d.by] ? (ps[d.by].name || 'Someone') : (shared.mode === 'local' ? 'you' : 'Someone')) + (d.at ? ' · ' + hhmm(d.at) : '')) : '';
        $('[data-bench-who="' + inp.dataset.bench + '"]').textContent = who;
      });
    });
  }
  async function saveShared(coll, id, rec) {
    rec.at = Date.now();
    if (caps.uid) rec.by = caps.uid;
    if (shared.mode === 'db') {
      try { await caps.db.collection(coll).doc(id).set(rec); } catch (err) { toast('Could not save: ' + (err && err.code || 'error')); }
    } else {
      shared[coll][id] = rec; local('hh-' + coll, shared[coll]); renderShared();
    }
  }
  $('#team').addEventListener('change', function (e) {
    var r = e.target.dataset.role;
    if (r) saveShared('team', r, { name: e.target.value.trim().slice(0, 60) });
  });
  $('#bench').addEventListener('change', function (e) {
    var b = e.target.dataset.bench;
    if (b) saveShared('bench', b, { value: e.target.value.trim().slice(0, 300) });
  });

  /* ---------------- inventory planner ---------------- */
  function renderInv() {
    var tk1 = num('#inv-tk1'), s0 = num('#inv-s0'), trip = num('#inv-trip'), pour = num('#inv-pour'), flush = num('#inv-flush'), lines = num('#inv-lines'), min = num('#inv-min'), brim = num('#inv-brim');
    var q1 = num('#inv-q1'), q2 = num('#inv-q2'), tp = num('#inv-tp'), tc1 = num('#inv-tc1'), smin = num('#inv-smin');
    var W = tk1 + s0, HOLD = 10;
    var c1 = W - trip - lines, endTyp = W + pour + flush - trip - lines, endWorst = W + pour + flush - 0.3 - lines;
    var card = function (k, v, ok, why, unit) { return '<div class="kv"><div class="k">' + k + '</div><div class="v">' + fx(v, unit === 's' ? 0 : 2) + ' <small>' + (unit || 'L') + '</small></div><div class="small">' + (ok ? '<span class="pill ok">ok</span>' : '<span class="pill bad">' + why + '</span>') + '</div></div>'; };
    var d = q2 - q1, before, sumpEnd, extra;
    if (d <= 0) {
      var u = -d, tTrip = u > 0 ? (trip - s0) / u * 60 : Infinity;
      before = Math.min(trip, s0 + u * tp / 60);
      sumpEnd = trip;
      extra = isFinite(tTrip) ? card('Float reaches trip before the pour at', tTrip, tTrip > tp, 'start the sump at ' + fx(trip - u * tp / 60 - 0.1, 2) + ' L', 's') : '';
    } else {
      before = s0 - d * tp / 60;
      sumpEnd = s0 + pour - d * tc1 / 60 - q1 * HOLD / 60;
      var tLate = (s0 + pour - trip - 0.1) / d * 60;
      extra = card('Latest pour that still trips LS-01', Math.max(tLate, 0), tLate >= tp, 'pour earlier or pour more', 's');
    }
    var trips = before + pour >= trip + 0.1, peak = before + pour;
    $('#inv-out').innerHTML =
      card('TK-01 during Case 1', c1, c1 >= min, 'add water to TK-01') +
      card('Sump just before the pour', before, before >= smin, 'P-02 will draw air') +
      card('Sump peak after pour', peak, peak <= 4.0, 'sump may overflow') +
      '<div class="kv"><div class="k">Pour trips LS-01?</div><div class="v">' + (trips ? 'yes' : 'no') + '</div><div class="small">' + (trips ? '<span class="pill ok">ok</span>' : '<span class="pill bad">pour earlier, pour more or raise the sump start</span>') + '</div></div>' +
      extra +
      card('Sump at end of Case 1', sumpEnd, sumpEnd >= smin, d > 0 ? 'shorten tc1 or pour more' : 'check') +
      card('TK-01 at end, typical', endTyp, endTyp <= brim - 0.5, 'start TK-01 lower') +
      card('TK-01 at end, worst', endWorst, endWorst <= brim - 0.3, 'start TK-01 lower') +
      '<div class="kv"><div class="k">Water to fill</div><div class="v">' + fx(W + flush, 2) + ' <small>L total</small></div><div class="small muted">TK-01 + sump + TK-03</div></div>';
    local('hh-inv-v3', INV_IDS.map(function (s) { return $(s).value; }));
  }
  var INV_IDS = ['#inv-tk1', '#inv-s0', '#inv-trip', '#inv-pour', '#inv-flush', '#inv-lines', '#inv-min', '#inv-brim', '#inv-q1', '#inv-q2', '#inv-tp', '#inv-tc1', '#inv-smin'];

  /* ---------------- P-01 duty finder ---------------- */
  var P1ROWS = 5;
  function p1Init() {
    var saved = local('hh-p1') || [];
    var duties = [40, 50, 60, 70, 100], tb = $('#p1-rows');
    for (var i = 0; i < P1ROWS; i++) {
      var s = saved[i] || {};
      var tr = document.createElement('tr');
      tr.innerHTML = '<td><input type="number" class="narrow" id="p1d' + i + '" aria-label="Duty, row ' + (i + 1) + '" value="' + (s.d != null ? s.d : duties[i]) + '"></td>' +
        '<td><input type="number" class="narrow" id="p1m' + i + '" aria-label="Mass, row ' + (i + 1) + '" value="' + (s.m != null ? s.m : '') + '" placeholder="g"></td>' +
        '<td><input type="number" class="narrow" id="p1t' + i + '" aria-label="Time, row ' + (i + 1) + '" value="' + (s.t != null ? s.t : 30) + '"></td>' +
        '<td class="num" id="p1q' + i + '">–</td>';
      tb.appendChild(tr);
    }
  }
  function renderP1() {
    var pts = [], save = [];
    for (var i = 0; i < P1ROWS; i++) {
      var d = num('#p1d' + i), m = num('#p1m' + i), t = num('#p1t' + i);
      save.push({ d: isFinite(d) ? d : null, m: isFinite(m) ? m : null, t: isFinite(t) ? t : null });
      var q = (m > 0 && t > 0) ? m / 1000 / t * 60 : NaN;
      $('#p1q' + i).textContent = fx(q, 3);
      if (q > 0 && d > 0) pts.push([d, q]);
    }
    local('hh-p1', save);
    var target = num('#p1-target'), margin = num('#p1-margin'), need = target * (1 + margin / 100);
    var gpm = target / 3.785, dpBar = Math.pow(gpm / 0.23, 2) * 0.0689;
    var html = '<div class="kv"><div class="k">P-01 must supply</div><div class="v">' + fx(need, 2) + ' <small>L/min</small></div></div>' +
      '<div class="kv"><div class="k">SOV-01 drop at ' + fx(target, 1) + ' L/min</div><div class="v">' + fx(dpBar, 2) + ' <small>bar (Cv 0.23)</small></div></div>';
    if (pts.length >= 2) {
      pts.sort(function (a, b) { return a[0] - b[0]; });
      var interpQ = function (x) {
        for (var k = 0; k < pts.length - 1; k++) if (x >= pts[k][0] && x <= pts[k + 1][0])
          return pts[k][1] + (x - pts[k][0]) * (pts[k + 1][1] - pts[k][1]) / (pts[k + 1][0] - pts[k][0]);
        return NaN;
      };
      var qmax = Math.max.apply(null, pts.map(function (p) { return p[1]; })), duty = NaN;
      if (need <= pts[0][1]) duty = pts[0][0];
      else for (var k = 0; k < pts.length - 1 && !isFinite(duty); k++)
        if (need > pts[k][1] && need <= pts[k + 1][1]) duty = pts[k][0] + (need - pts[k][1]) * (pts[k + 1][0] - pts[k][0]) / (pts[k + 1][1] - pts[k][1]);
      var reach = isFinite(duty), q50 = interpQ(50), top = pts[pts.length - 1], hi = pts.filter(function (p) { return p[0] >= 65 && p[0] <= 75; })[0];
      html += '<div class="kv"><div class="k">At 50% duty</div><div class="v">' + fx(q50, 2) + ' <small>L/min</small></div><div class="small">' + (!isFinite(q50) ? '<span class="pill warn">measure 50%</span>' : q50 >= need ? '<span class="pill ok">spec duty works</span>' : '<span class="pill warn">raise d1</span>') + '</div></div>' +
        '<div class="kv"><div class="k">Duty for ' + fx(need, 2) + ' L/min</div><div class="v">' + (reach ? fx(duty, 0) + ' %' : 'not reached') + '</div><div class="small">' + (reach ? '' : '<span class="pill bad">P-01 tops out at ' + fx(qmax, 2) + ' L/min: inventory planner, sheet 03</span>') + '</div></div>';
      if (hi && top[0] >= 95 && top[1] < 1.1 * hi[1]) html += '<div class="kv"><div class="k">Flow above 70%</div><div class="v">flat</div><div class="small"><span class="pill warn">suction-limited by SOV-01: more duty will not help</span></div></div>';
      var d1 = isFinite(q50) && q50 >= need ? 0.5 : Math.min(1, Math.ceil(duty) / 100);
      $('#p1-cmd').textContent = reach ? 'SET d1 ' + d1.toFixed(2) + '\nSET d1f ' + d1.toFixed(2) + '\nSAVE' : 'P-01 cannot reach ' + need.toFixed(2) + ' L/min. SET d1 1.00, SET d1f 1.00, SAVE, then enter ' + qmax.toFixed(2) + ' L/min as P-01 flow in the inventory planner (sheet 03).';
    } else {
      $('#p1-cmd').textContent = 'Enter at least two duties.';
    }
    $('#p1-out').innerHTML = html;
  }

  /* ---------------- Q1.2 velocity ---------------- */
  function flowRow(qLpm, dMm) {
    var q = qLpm / 60000, d = dMm / 1000, A = Math.PI * d * d / 4, v = q / A, re = 1000 * v * d / 1e-3;
    var f = re < 2300 ? 64 / re : 0.316 * Math.pow(re, -0.25);
    return { v: v, re: re, regime: re < 2300 ? 'laminar' : re < 4000 ? 'transitional' : re < 6000 ? 'turbulent, near transition' : 'turbulent', dp: f * 1000 * v * v / (2 * d) / 1000, tt: 1 / v };
  }
  function renderVel() {
    var nom = num('#v-nom'), id = num('#v-id');
    var targets = [[1, '#v-q1'], [3, '#v-q3'], [6, '#v-q6']];
    $('#v-rows').innerHTML = targets.map(function (t) {
      var ach = num(t[1]), q = ach > 0 ? ach : t[0];
      var a = flowRow(t[0], nom), b = flowRow(q, id);
      return '<tr><td>' + t[0] + ' L/min' + (ach > 0 ? ' <span class="muted small">(achieved ' + fx(ach, 2) + ')</span>' : '') + '</td><td class="num">' + fx(a.v, 3) + '</td><td class="num">' + Math.round(a.re).toLocaleString() + '</td><td class="num">' + fx(b.v, 3) + '</td><td class="num">' + Math.round(b.re).toLocaleString() + '</td><td>' + b.regime + '</td><td class="num">' + fx(b.dp, 1) + '</td><td class="num">' + fx(b.tt, 2) + '</td></tr>';
    }).join('');
    local('hh-vel', ['#v-nom', '#v-id', '#v-q1', '#v-q3', '#v-q6'].map(function (s) { return $(s).value; }));
  }

  /* ---------------- Q3.1 residence ---------------- */
  function renderRes() {
    var V = num('#r-v'), Q = num('#r-q'), tau = V / Q * 60;
    var kv = function (k, v, u) { return '<div class="kv"><div class="k">' + k + '</div><div class="v">' + v + ' <small>' + u + '</small></div></div>'; };
    $('#r-out').innerHTML = kv('τ = V/Q', fx(tau, 1), 's') + kv('V doubled', fx(tau * 2, 1), 's') + kv('Q doubled', fx(tau / 2, 1), 's') + kv('Turnover Q/V', fx(Q / V, 2), 'per min');
    var s = num('#r-sump'), fl = num('#r-flush');
    $('#r-wash').innerHTML = kv('Sump residence at Q', fx(s / Q * 60, 0), 's') + kv('Original fluid left', fx(Math.exp(-fl / s) * 100, 0), '% after flush');
  }

  /* ---------------- diagnoser ---------------- */
  var DX = {
    off_zero: ['Normal: pump off (Condition D)', 'If the pump was commanded on, check the driver enable, the fuse and the motor current.'],
    off_pulses: ['SPURIOUS_PULSES', 'Siphoning through the pump, or interference on the pulse line. Check whether the return line drains back, and route the sensor lead away from the motor wires.'],
    normal_normal: ['NORMAL (Condition A)', 'Nothing to do.'],
    normal_high: ['Running against higher pressure', 'BV-02 is partly closed or the outlet is restricted. Flow still holds because the pump is positive-displacement.'],
    normal_low: ['Early loss of suction', 'Sump level is low or air is getting in at a suction joint. Watch for bubbles in L-201.'],
    normal_zero: ['Current-sense fault', 'The flow is real, so check the IS wiring and the gain.'],
    normal_fluct: ['Watch: air entrainment starting', 'Check the sump level and the dip-tube depth.'],
    reduced_high: ['RESTRICTION (Condition B)', 'Valve partly closed, a kink, or a partial blockage. Open BV-02 and see if the flow recovers.'],
    reduced_low: ['Partial loss of suction', 'Air leak on the suction side, low sump, or BV-03 partly closed.'],
    reduced_normal: ['FT-01 suspect', 'The pump load is normal while the flow reads low. Check the pulse duty (~50%), the sensor supply and the connector.'],
    reduced_fluct: ['UNSTABLE_FLOW', 'Air drawn in or cavitation. Check the sump level and the suction joints.'],
    zero_high: ['DISCHARGE_BLOCKED (Condition C)', 'Closed valve or blocked outlet; the pressure switch is cycling. Firmware trips P-02 after 3 s.'],
    zero_low: ['SUCTION_LOSS (Condition C)', 'Dry sump, air lock, or BV-03 shut. Firmware trips after 5 s and retries.'],
    zero_zero: ['PUMP_FAILURE (Condition C or D)', 'Motor, driver, fuse or wiring. Check 12 V at the IBT-2 B+ terminal and the EN lines.'],
    zero_normal: ['FT01_SIGNAL_FAILURE (Condition C)', 'The pump is loaded normally, so fluid is moving. Check the sensor wiring, its 5 V supply and the divider.'],
    zero_fluct: ['DISCHARGE_BLOCKED, pressure switch cycling', 'Open the outlet. The pump is dead-heading against its 8.25 bar switch.'],
    intermittent_fluct: ['UNSTABLE_FLOW (Condition E)', 'Air entrainment, cavitation or pressure-switch cycling. Raise the sump level and check the suction joints.'],
    intermittent_normal: ['FT01_INTERMITTENT (Condition E)', 'The pump load is steady, so the signal is at fault: a loose connector or interference.'],
    intermittent_high: ['Pressure switch cycling near dead-head (Condition E)', 'Open BV-02.'],
    intermittent_low: ['Air entrainment, low sump (Condition E)', 'Raise the sump level and check the dip tube.'],
    intermittent_zero: ['Pump cutting in and out', 'Check the motor leads and the driver enable.']
  };
  var UNKNOWN = {
    zero: ['NO_FLOW_CAUSE_UNKNOWN (Condition C)', 'FT-01 alone cannot separate these: blocked line, dry or air-locked pump, failed pump, failed sensor. Measure pump current, look at the tubing, check the sump level.'],
    reduced: ['Condition B: likely a valve restriction', 'Confirm with pump current (it should rise) or by reopening BV-02.'],
    intermittent: ['Condition E: unstable flow or an intermittent signal', 'Pump current separates them: fluctuating current means hydraulic; steady current means sensor.'],
    normal: ['NORMAL (Condition A)', 'Nothing to do.']
  };
  function renderDx() {
    var p = $('#dg-pump').value, pu = $('#dg-pulse').value, c = $('#dg-cur').value, r;
    if (p === 'off') r = pu === 'zero' ? DX.off_zero : DX.off_pulses;
    else if (c === 'unknown') r = UNKNOWN[pu];
    else r = DX[pu + '_' + c] || ['No rule', 'Combination not covered.'];
    $('#dg-out').innerHTML = '<h3>' + esc(r[0]) + '</h3><p>' + esc(r[1]) + '</p>';
  }

  /* ---------------- downloads ---------------- */
  async function saveFile(filename, data) {
    var note = $('#dl-note');
    if (!caps.downloads) { note.textContent = 'Downloads are not available in this view.'; return; }
    try { await caps.downloads.save({ filename: filename, data: data }); note.textContent = 'Saved ' + filename + '.'; }
    catch (err) { if (!err || err.code !== 'declined') note.textContent = 'Could not save ' + filename + ' (' + (err && err.code || 'error') + ').'; }
  }
  async function packZip(manifestPath, filename) {
    var note = $('#dl-note');
    if (!caps.downloads) { note.textContent = 'Downloads are not available in this view.'; return; }
    if (!window.JSZip) { note.textContent = 'The zip library did not load. Reload the page and try again.'; return; }
    note.textContent = 'Packing ' + filename + '...';
    try {
      var manifest = await (await fetch(manifestPath)).json();
      var zip = new window.JSZip(), cache = {};
      for (var arc in manifest) {
        var pub = manifest[arc];
        if (!cache[pub]) { var r = await fetch(pub); if (!r.ok) throw { code: 'missing ' + pub }; cache[pub] = await r.text(); }
        zip.file(arc, cache[pub]);
      }
      var blob = await zip.generateAsync({ type: 'blob', compression: 'DEFLATE' });
      note.textContent = '';
      await saveFile(filename, blob);
    } catch (err) { note.textContent = 'Could not pack ' + filename + ' (' + (err && err.code || 'error') + ').'; }
  }
  $('#dl-kit').addEventListener('click', function () { packZip('kit/manifest.json', 'hh-build-kit.zip'); });
  $('#dl-share').addEventListener('click', function () { packZip('kit/share_manifest.json', 'lam-flow-rig-code.zip'); });
  [['#dl-pid', 'kit/pid.svg', 'hh-pid.svg'], ['#dl-wiring', 'kit/wiring.svg', 'hh-wiring-E01.svg'], ['#dl-labels', 'kit/tag_labels.svg', 'hh-tag-labels.svg'],
    ['#dl-dial', 'kit/bv02_dial.svg', 'hh-bv02-dial.svg']].forEach(function (d) {
    $(d[0]).addEventListener('click', async function () {
      try { var r = await fetch(d[1]); if (!r.ok) throw r; await saveFile(d[2], await r.text()); }
      catch (err) { $('#dl-note').textContent = 'Could not load ' + d[2] + '.'; }
    });
  });

  /* ---------------- boot ---------------- */
  (function restore() {
    var inv = local('hh-inv-v3');
    if (inv) INV_IDS.forEach(function (s, i) { if (inv[i] !== '' && inv[i] != null) $(s).value = inv[i]; });
    var vel = local('hh-vel');
    if (vel) ['#v-nom', '#v-id', '#v-q1', '#v-q3', '#v-q6'].forEach(function (s, i) { if (vel[i] != null) $(s).value = vel[i]; });
  })();
  p1Init();
  ['#inventory', '#p1duty', '#velocity', '#residence'].forEach(function (s) { $(s).addEventListener('input', function () { renderInv(); renderP1(); renderVel(); renderRes(); }); });
  ['#dg-pump', '#dg-pulse', '#dg-cur'].forEach(function (s) { $(s).addEventListener('change', renderDx); });
  renderInv(); renderP1(); renderVel(); renderRes(); renderDx();

  cal.runs = local('hh-cal-runs') || [];
  chk.state = local('hh-checks') || {};
  shared.team = local('hh-team') || {};
  shared.bench = local('hh-bench') || {};
  renderCal();
  renderChecks();
  renderShared();

  ready.then(async function (res) {
    caps.db = res[0]; caps.user = res[1]; caps.downloads = res[2];
    if (!caps.downloads) { $('#dl-note').textContent = 'Downloads are not available in this view.'; }
    if (caps.user) { try { caps.uid = await caps.user.id(); } catch (e) { caps.uid = null; } }
    if (!caps.db) {
      $('#cal-sync').textContent = 'Saved in this browser only (shared storage is not available in this view).';
      $('#chk-mode').textContent = 'Ticks are saved in this browser only, because shared storage is not available in this view.';
      $('#bench-mode').textContent = 'Saved in this browser only (shared storage is not available in this view).';
      return;
    }
    cal.mode = 'db'; chk.mode = 'db'; shared.mode = 'db';
    $('#bench-mode').textContent = 'Shared: every teammate sees each entry live, with who entered it and when.';
    ['team', 'bench'].forEach(function (coll) {
      caps.db.collection(coll).onSnapshot(function (snap) {
        var st = {};
        snap.docs.forEach(function (d) { st[d.id] = d.data(); });
        shared[coll] = st;
        renderShared();
      }, function () { $('#bench-mode').textContent = 'Lost the connection to shared storage. Reload the page.'; });
    });
    $('#cal-sync').textContent = 'Shared: every teammate sees the same runs live.';
    $('#chk-mode').textContent = 'Shared: every tick shows who made it and when, live for the whole team.';
    caps.db.collection('cal_runs').orderBy('at').onSnapshot(function (snap) {
      cal.runs = snap.docs.map(function (d) { var o = Object.assign({}, d.data()); o.id = d.id; return o; });
      renderCal();
    }, function () { $('#cal-sync').textContent = 'Lost the connection to shared storage. Reload the page.'; });
    caps.db.collection('checks').onSnapshot(function (snap) {
      var st = {};
      snap.docs.forEach(function (d) { st[d.id] = d.data(); });
      chk.state = st;
      renderChecks();
    }, function () { $('#chk-mode').textContent = 'Lost the connection to shared storage. Reload the page.'; });
  });
})();
