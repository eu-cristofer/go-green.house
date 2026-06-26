# 🎂 Aniversário

```{raw} html
<div id="bday-card" style="
    max-width: 620px; margin: 1rem auto; padding: 2rem 1.5rem;
    background: #f3fbf8; border: 1px solid #d4efe6; border-radius: 18px;
    text-align: center; font-family: -apple-system, Segoe UI, Roboto, sans-serif;
    position: relative; overflow: hidden;">

  <div class="balloons" aria-hidden="true" style="position:absolute; inset:0; pointer-events:none;">
    <span>🎈</span><span>🎈</span><span>🎈</span><span>🎈</span><span>🎈</span>
  </div>

  <div style="position: relative; z-index: 1;">
    <div style="font-size: 0.95rem; color: #0f6e56; letter-spacing: .02em;">🎂 Maria &amp; Sofia</div>
    <h2 id="bday-turning" style="margin: .35rem 0 1.4rem; font-size: 1.35rem; color: #04342c; font-weight: 600;">&nbsp;</h2>

    <div id="bday-count" style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 1.4rem;">
      <div class="b-unit"><div id="b-d" class="b-num">–</div><div class="b-lbl">dias</div></div>
      <div class="b-unit"><div id="b-h" class="b-num">–</div><div class="b-lbl">horas</div></div>
      <div class="b-unit"><div id="b-m" class="b-num">–</div><div class="b-lbl">min</div></div>
      <div class="b-unit"><div id="b-s" class="b-num">–</div><div class="b-lbl">seg</div></div>
    </div>

    <p id="bday-age" style="margin: 0; font-size: .9rem; color: #5b6b66;">&nbsp;</p>
    <p id="bday-since" style="margin: .5rem 0 0; font-size: .85rem; color: #0f6e56;">&nbsp;</p>
    <p id="bday-date" style="margin: .5rem 0 0; font-size: .8rem; color: #8aa39b;">16 de outubro</p>
  </div>
</div>

<style>
  #bday-card .b-unit { background: #ffffff; border: 1px solid #e3f2ec; border-radius: 12px; padding: .85rem .25rem; }
  #bday-card .b-num  { font-size: 1.9rem; font-weight: 700; color: #1abc9c; line-height: 1.1; }
  #bday-card .b-lbl  { font-size: .75rem; color: #7c8c87; margin-top: .15rem; }
  #bday-card .balloons span {
    position: absolute; bottom: -40px; font-size: 1.6rem; opacity: .55;
    animation: bday-float 9s linear infinite;
  }
  #bday-card .balloons span:nth-child(1){ left: 6%;  animation-delay: 0s;   }
  #bday-card .balloons span:nth-child(2){ left: 26%; animation-delay: 2.2s; }
  #bday-card .balloons span:nth-child(3){ left: 50%; animation-delay: 4s;   }
  #bday-card .balloons span:nth-child(4){ left: 72%; animation-delay: 1.2s; }
  #bday-card .balloons span:nth-child(5){ left: 90%; animation-delay: 3.3s; }
  @keyframes bday-float {
    0%   { transform: translateY(0) rotate(-4deg);   opacity: 0; }
    15%  { opacity: .55; }
    100% { transform: translateY(-260px) rotate(4deg); opacity: 0; }
  }
  @media (prefers-reduced-motion: reduce) {
    #bday-card .balloons span { animation: none; display: none; }
  }
</style>

<script>
(function(){
  // === Configuração: data de nascimento das gêmeas (ano, mês 1–12, dia) ===
  // Maria e Sofia nasceram no mesmo dia. Para datas diferentes, é só
  // duplicar este bloco com outro id de card.
  var BIRTH = { year: 2022, month: 10, day: 16 };

  function $(id){ return document.getElementById(id); }
  function pad(n){ return (n < 10 ? "0" : "") + n; }

  function tick(){
    var now = new Date();
    var today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    var next = new Date(now.getFullYear(), BIRTH.month - 1, BIRTH.day, 0, 0, 0);
    if (next < today) { next = new Date(now.getFullYear() + 1, BIRTH.month - 1, BIRTH.day); }
    var turningAge = next.getFullYear() - BIRTH.year;

    // Tempo de vida: dias e meses completos desde o nascimento
    var bornAt = new Date(BIRTH.year, BIRTH.month - 1, BIRTH.day);
    var daysAlive = Math.floor((today - bornAt) / 86400000);
    var months = (now.getFullYear() - BIRTH.year) * 12 + (now.getMonth() - (BIRTH.month - 1));
    if (now.getDate() < BIRTH.day) months -= 1;
    $("bday-since").textContent = "🌱 " + daysAlive.toLocaleString("pt-BR") +
      " dias de vida · " + months + " meses";

    var isBirthday = (now.getMonth() === BIRTH.month - 1 && now.getDate() === BIRTH.day);
    if (isBirthday) {
      $("bday-turning").textContent = "🎉 Hoje é aniversário! " + turningAge + " anos 🎉";
      $("b-d").textContent = $("b-h").textContent = $("b-m").textContent = $("b-s").textContent = "0";
      $("bday-age").textContent = "Feliz aniversário, Maria e Sofia! 💖";
      return;
    }

    var diff = Math.max(0, next - now);
    $("bday-turning").textContent = "Faltam para os " + turningAge + " anos";
    $("b-d").textContent = Math.floor(diff / 86400000);
    $("b-h").textContent = pad(Math.floor((diff % 86400000) / 3600000));
    $("b-m").textContent = pad(Math.floor((diff % 3600000) / 60000));
    $("b-s").textContent = pad(Math.floor((diff % 60000) / 1000));

    var ageY = now.getFullYear() - BIRTH.year;
    var hadBday = (now.getMonth() > BIRTH.month - 1) ||
                  (now.getMonth() === BIRTH.month - 1 && now.getDate() >= BIRTH.day);
    if (!hadBday) ageY -= 1;
    $("bday-age").textContent = "Hoje elas têm " + ageY + " anos.";
  }

  tick();
  setInterval(tick, 1000);
})();
</script>
```
