with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

target = '''          <div class="canvas-container">
            <canvas id="laserCanvas"></canvas>
            <div id="canvasInfo" class="canvas-overlay-info">
              SYSTEM: Nd:YAG PULSED (1064 nm) · DRAG TO ROTATE · SCROLL TO ZOOM
            </div>
          </div>'''

replacement = '''          <div style="display:flex; gap:0.5rem; margin-bottom:0.5rem;">
            <button id="view3dBtn" class="selector-btn active" onclick="setViewMode('3d')">Interactive 3D Exploded View</button>
            <button id="viewCadBtn" class="selector-btn" onclick="setViewMode('cad')">Photorealistic CAD Visual</button>
          </div>
          <div class="canvas-container" id="canvasWrap">
            <canvas id="laserCanvas"></canvas>
            <div id="canvasInfo" class="canvas-overlay-info">
              SYSTEM: Nd:YAG PULSED (1064 nm) · DRAG TO ROTATE · SCROLL TO ZOOM
            </div>
          </div>
          <div id="cadWrap" style="display:none; width:100%; height:480px; background:#090e17; border-radius:8px; overflow:hidden; border:1px solid rgba(255,255,255,0.08); text-align:center;">
            <img id="cadImg" src="annotated_ndyag_render.jpg" style="height:100%; max-width:100%; object-fit:contain;" alt="CAD render">
          </div>'''

js_target = 'function selectApparatus(app) {'
js_replacement = '''function setViewMode(mode) {
      document.getElementById('view3dBtn').classList.toggle('active', mode === '3d');
      document.getElementById('viewCadBtn').classList.toggle('active', mode === 'cad');
      document.getElementById('canvasWrap').style.display = mode === '3d' ? 'block' : 'none';
      document.getElementById('cadWrap').style.display = mode === 'cad' ? 'block' : 'none';
      if (mode === 'cad') {
        document.getElementById('cadImg').src = currentApparatus === 'ndyag' ? 'annotated_ndyag_render.jpg' : 'annotated_fiber_render.jpg';
      }
    }

    function selectApparatus(app) {
      if (document.getElementById('cadWrap').style.display === 'block') {
        document.getElementById('cadImg').src = app === 'ndyag' ? 'annotated_ndyag_render.jpg' : 'annotated_fiber_render.jpg';
      }'''

if target in c:
    c = c.replace(target, replacement)
    c = c.replace(js_target, js_replacement)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(c)
    print("SUCCESS: index.html updated!")
else:
    print("Target not found in index.html")
