import os
import urllib.request
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# ── Data: World Happiness Report 2025 ─────────────────────────────────────────
happiness = {
    'Finland': 7.764,
    'Denmark': 7.539,
    'Iceland': 7.540,
    'Sweden':  7.255,
    'Norway':  7.242,
}

label_offsets = {
    'Finland':  (0,    0.5),
    'Denmark':  (0,    0.3),
    'Iceland':  (-2,   0.5),
    'Sweden':   (0,    0.5),
    'Norway':   (-1.5, 0.5),
}
score_offsets = {
    'Finland':  (0,   -1.2),
    'Denmark':  (0,   -1.0),
    'Iceland':  (-2,  -1.2),
    'Sweden':   (0,   -1.2),
    'Norway':   (-1.5,-1.2),
}

# ── Auto-download country borders ─────────────────────────────────────────────
geojson_path = 'countries.geojson'
if not os.path.exists(geojson_path):
    url = ('https://raw.githubusercontent.com/nvkelso/natural-earth-vector'
           '/master/geojson/ne_110m_admin_0_countries.geojson')
    print('Downloading country borders...')
    urllib.request.urlretrieve(url, geojson_path)
    print('Done.')

world = gpd.read_file(geojson_path)
nordic = world[world['NAME'].isin(happiness.keys())].copy()
nordic['happiness'] = nordic['NAME'].map(happiness)

# ── Color map ─────────────────────────────────────────────────────────────────
cmap = mcolors.LinearSegmentedColormap.from_list(
    'happiness_green', ['#C8E6C9','#66BB6A','#2E7D32','#1B5E20'], N=512)
vmin, vmax = 7.25, 7.80
norm = mcolors.Normalize(vmin=vmin, vmax=vmax)

# ── Plot ──────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 11))
fig.patch.set_facecolor('#D6EAF8')
ax.set_facecolor('#D6EAF8')

world_bg = world[~world['NAME'].isin(happiness.keys())]
world_bg.plot(ax=ax, color='#E8E8E8', edgecolor='#CCCCCC', linewidth=0.4)
nordic.plot(ax=ax, column='happiness', cmap=cmap, vmin=vmin, vmax=vmax,
            edgecolor='white', linewidth=1.5)

for _, row in nordic.iterrows():
    cx = row.geometry.centroid.x
    cy = row.geometry.centroid.y
    name = row['NAME']
    score = happiness[name]
    dx_l, dy_l = label_offsets[name]
    dx_s, dy_s = score_offsets[name]

    ax.text(cx + dx_l, cy + dy_l, name,
            ha='center', va='center',
            fontsize=11, fontweight='bold', color='white',
            bbox=dict(boxstyle='round,pad=0.35', facecolor='#1B5E20',
                      alpha=0.85, edgecolor='white', linewidth=1))

    ax.text(cx + dx_s, cy + dy_s, f'{score:.2f}',
            ha='center', va='center',
            fontsize=11, fontweight='bold', color='white',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#333333',
                      alpha=0.75, edgecolor='none'))

# ── Colorbar ──────────────────────────────────────────────────────────────────
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, orientation='vertical',
                    fraction=0.025, pad=0.02, shrink=0.6)
cbar.set_label('Happiness Score', fontsize=10, color='#333')
cbar.ax.tick_params(labelsize=9, colors='#333')
cbar.outline.set_visible(False)

ax.set_xlim(-25, 32)
ax.set_ylim(54, 72)
ax.axis('off')

ax.set_title('Happiness Score in Nordic Countries, 2025',
             fontsize=15, fontweight='bold', color='#1a1a1a', pad=14)
fig.text(0.99, 0.01,
         'Source: World Happiness Report 2025 (Gallup/UN) | worldhappiness.report',
         ha='right', fontsize=8, color='#555')

plt.tight_layout()
plt.savefig('nordic_happiness_map.png', dpi=150,
            bbox_inches='tight', facecolor=fig.get_facecolor())
print('Saved: nordic_happiness_map.png')
plt.show()