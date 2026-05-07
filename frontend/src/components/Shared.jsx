import React from 'react';

// ── Prix FCFA ─────────────────────────────────────────────────────────────────
export const toCFA = (price) => {
  return Math.round(price || 0).toLocaleString('fr-FR').replace(/\s/g, '.') + ' FCFA';
};

// ── Design tokens ─────────────────────────────────────────────────────────────
export const C = {
  bg: '#09090B',
  surface: '#111113',
  border: '#27272A',
  border2: '#1e1e21',
  gold: '#C9A96E',
  goldDim: 'rgba(201,169,110,0.1)',
  goldBorder: 'rgba(201,169,110,0.4)',
  text: '#FAFAFA',
  muted: '#71717A',
  subtle: '#52525B',
  faint: '#3f3f46',
  error: '#e05c5c',
  playfair: "'Playfair Display', serif",
  dm: "'DM Sans', sans-serif",
};

// ── Senegal Flag ──────────────────────────────────────────────────────────────
export const SenegalFlag = ({ size = 18 }) => (
  <svg width={size * 1.5} height={size} viewBox="0 0 30 20" style={{ borderRadius: 2, flexShrink: 0 }}>
    <rect width="10" height="20" fill="#00853F" />
    <rect x="10" width="10" height="20" fill="#FDEF42" />
    <rect x="20" width="10" height="20" fill="#E31B23" />
    <polygon
      points="15,6.5 16.18,10.09 19.94,10.09 16.88,12.27 18.06,15.86 15,13.68 11.94,15.86 13.12,12.27 10.06,10.09 13.82,10.09"
      fill="#00853F"
    />
  </svg>
);

// ── Logo Icon SVG (double anneau avec glow) ───────────────────────────────────
const LogoIcon = ({ size }) => (
  <svg width={size} height={size * 0.75} viewBox="0 0 80 60" fill="none">
    <defs>
      <filter id="goldGlow" x="-40%" y="-40%" width="180%" height="180%">
        <feGaussianBlur stdDeviation="2.5" result="blur" />
        <feMerge>
          <feMergeNode in="blur" />
          <feMergeNode in="SourceGraphic" />
        </feMerge>
      </filter>
      <radialGradient id="ringGrad" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stopColor="#F0D898" />
        <stop offset="60%" stopColor="#C9A96E" />
        <stop offset="100%" stopColor="#9B7A3F" />
      </radialGradient>
    </defs>
    {/* Anneau gauche */}
    <circle cx="28" cy="30" r="20" stroke="url(#ringGrad)" strokeWidth="1.8" filter="url(#goldGlow)" />
    {/* Anneau droit */}
    <circle cx="52" cy="30" r="20" stroke="url(#ringGrad)" strokeWidth="1.8" filter="url(#goldGlow)" />
    {/* Emblème central */}
    <circle cx="40" cy="30" r="7.5" stroke="#C9A96E" strokeWidth="1.2" />
    <circle cx="40" cy="30" r="2.2" fill="#C9A96E" />
    <line x1="40" y1="22.5" x2="40" y2="37.5" stroke="#C9A96E" strokeWidth="0.8" />
    <line x1="32.5" y1="30" x2="47.5" y2="30" stroke="#C9A96E" strokeWidth="0.8" />
    <line x1="35" y1="24.8" x2="45" y2="35.2" stroke="#C9A96E" strokeWidth="0.6" />
    <line x1="45" y1="24.8" x2="35" y2="35.2" stroke="#C9A96E" strokeWidth="0.6" />
  </svg>
);

// ── Logo ──────────────────────────────────────────────────────────────────────
export const Logo = ({ size = 'md', onClick }) => {
  const cfg = {
    sm: { icon: 36, titleSize: 14, taglineSize: 8,  flagSize: 13, gap: 8,  showTagline: false },
    md: { icon: 48, titleSize: 18, taglineSize: 9,  flagSize: 16, gap: 10, showTagline: false },
    lg: { icon: 72, titleSize: 28, taglineSize: 10, flagSize: 20, gap: 16, showTagline: true  },
  };
  const s = cfg[size] || cfg.md;

  return (
    <div
      onClick={onClick}
      style={{ display: 'flex', alignItems: 'center', gap: s.gap, cursor: onClick ? 'pointer' : 'default' }}
    >
      <LogoIcon size={s.icon} />

      <div style={{ display: 'flex', flexDirection: 'column', gap: 0 }}>
        {/* Titre */}
        <span style={{ fontFamily: C.playfair, fontSize: s.titleSize, fontWeight: 700, letterSpacing: '0.01em', lineHeight: 1.1, whiteSpace: 'nowrap' }}>
          <span style={{ color: C.text }}>Auto</span>
          <span style={{ color: C.gold }}> Connect</span>
        </span>

        {/* Ligne dorée + tagline — uniquement en lg */}
        {s.showTagline && (
          <>
            <div style={{ height: 1, background: `linear-gradient(to right, ${C.gold}, rgba(201,169,110,0.2))`, margin: '5px 0 5px' }} />
            <span style={{ fontFamily: C.dm, fontSize: s.taglineSize, color: C.muted, letterSpacing: '0.22em', textTransform: 'uppercase', whiteSpace: 'nowrap' }}>
              Trouvez · Essayez · Achetez
            </span>
          </>
        )}
      </div>

      {/* Séparateur vertical + drapeau — uniquement en lg */}
      {s.showTagline && (
        <>
          <div style={{ width: 1, height: 48, background: `rgba(201,169,110,0.3)`, margin: '0 6px' }} />
          <SenegalFlag size={s.flagSize} />
        </>
      )}

      {/* Drapeau compact pour sm/md */}
      {!s.showTagline && <SenegalFlag size={s.flagSize} />}
    </div>
  );
};

// ── Navbar ────────────────────────────────────────────────────────────────────
export const Navbar = ({ user, navigate, currentView, onLogout }) => {
  const [menuOpen, setMenuOpen] = React.useState(false);
  const menuRef = React.useRef(null);

  // Ferme le menu quand on clique ailleurs
  React.useEffect(() => {
    if (!menuOpen) return;
    const onClick = (e) => {
      if (menuRef.current && !menuRef.current.contains(e.target)) setMenuOpen(false);
    };
    document.addEventListener('mousedown', onClick);
    return () => document.removeEventListener('mousedown', onClick);
  }, [menuOpen]);

  const navLinks = [
    { label: 'Catalogue', view: 'catalogue' },
    { label: 'Comment ça marche', view: 'how' },
  ];

  return (
    <nav style={{
      position: 'fixed', top: 0, left: 0, right: 0, zIndex: 100,
      background: 'rgba(9,9,11,0.85)', backdropFilter: 'blur(16px)',
      borderBottom: `1px solid ${C.border2}`, height: 64,
      display: 'flex', alignItems: 'center', padding: '0 32px',
    }}>
      <Logo size="md" onClick={() => navigate('home')} />

      <div style={{ flex: 1 }} />

      <div style={{ display: 'flex', alignItems: 'center', gap: 28 }}>
        {navLinks.map(l => (
          <button key={l.view} onClick={() => navigate(l.view)} style={{
            background: 'none', border: 'none',
            color: currentView === l.view ? C.gold : C.muted,
            fontFamily: C.dm, fontSize: 14, fontWeight: 500, cursor: 'pointer',
            transition: 'color 0.2s',
          }}>{l.label}</button>
        ))}

        {user ? (
          <div ref={menuRef} style={{ display: 'flex', gap: 10, alignItems: 'center', position: 'relative' }}>
            {(user.is_staff || user.user_type === 'admin') && (
              <button onClick={() => navigate('admin-dashboard')} style={{
                background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.35)',
                color: '#f87171', fontFamily: C.dm, fontSize: 11, fontWeight: 700,
                padding: '6px 12px', borderRadius: 8, cursor: 'pointer', letterSpacing: '0.04em',
              }}>⚙ ADMIN</button>
            )}
            <button
              onClick={() => setMenuOpen(o => !o)}
              style={{
                background: C.goldDim, border: `1px solid ${C.goldBorder}`,
                color: C.gold, fontFamily: C.dm, fontSize: 13, fontWeight: 600,
                padding: '8px 14px', borderRadius: 8, cursor: 'pointer',
                display: 'flex', alignItems: 'center', gap: 8,
              }}
            >
              <span style={{
                width: 28, height: 28, borderRadius: '50%',
                background: C.gold, color: C.bg, fontSize: 11, fontWeight: 700,
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                overflow: 'hidden', flexShrink: 0,
              }}>
                {user.avatar_url
                  ? <img src={user.avatar_url} alt="" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                  : (user.avatar_initials || (user.first_name?.[0] || 'U').toUpperCase())
                }
              </span>
              {user.first_name || 'Mon espace'}
              <span style={{ fontSize: 9, opacity: 0.7 }}>▾</span>
            </button>

            {menuOpen && (
              <div style={{
                position: 'absolute', top: 48, right: 0, minWidth: 220,
                background: C.surface, border: `1px solid ${C.border}`,
                borderRadius: 12, padding: 6, boxShadow: '0 12px 32px rgba(0,0,0,0.5)',
                zIndex: 200,
              }}>
                <div style={{
                  padding: '10px 14px', borderBottom: `1px solid ${C.border2}`, marginBottom: 4,
                }}>
                  <div style={{ fontFamily: C.dm, fontSize: 13, color: C.text, fontWeight: 600 }}>
                    {user.first_name} {user.last_name}
                  </div>
                  <div style={{ fontFamily: C.dm, fontSize: 11, color: C.muted, marginTop: 2 }}>
                    {user.email}
                  </div>
                </div>

                {[
                  { label: '📊  Mon tableau de bord', action: () => navigate(user.user_type === 'seller' ? 'seller-dashboard' : user.user_type === 'admin' ? 'admin-dashboard' : 'buyer-dashboard') },
                  { label: '⚙️  Paramètres',          action: () => navigate('settings') },
                ].map(item => (
                  <button key={item.label}
                    onClick={() => { setMenuOpen(false); item.action(); }}
                    style={{
                      width: '100%', textAlign: 'left', background: 'none', border: 'none',
                      color: C.text, fontFamily: C.dm, fontSize: 13,
                      padding: '10px 14px', borderRadius: 8, cursor: 'pointer',
                    }}
                    onMouseEnter={e => e.currentTarget.style.background = C.border2}
                    onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
                  >{item.label}</button>
                ))}

                <div style={{ height: 1, background: C.border2, margin: '4px 0' }} />

                <button
                  onClick={() => { setMenuOpen(false); onLogout && onLogout(); }}
                  style={{
                    width: '100%', textAlign: 'left', background: 'none', border: 'none',
                    color: C.error, fontFamily: C.dm, fontSize: 13, fontWeight: 600,
                    padding: '10px 14px', borderRadius: 8, cursor: 'pointer',
                  }}
                  onMouseEnter={e => e.currentTarget.style.background = 'rgba(224,92,92,0.08)'}
                  onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
                >↪ Se déconnecter</button>
              </div>
            )}
          </div>
        ) : (
          <div style={{ display: 'flex', gap: 10 }}>
            <button onClick={() => navigate('auth', { mode: 'login' })} style={{
              background: 'none', border: `1px solid ${C.border}`,
              color: C.text, fontFamily: C.dm, fontSize: 14, fontWeight: 500,
              padding: '8px 16px', borderRadius: 8, cursor: 'pointer',
              transition: 'border-color 0.2s',
            }}>Connexion</button>
            <button onClick={() => navigate('auth', { mode: 'register' })} style={{
              background: C.gold, border: 'none', color: C.bg,
              fontFamily: C.dm, fontSize: 14, fontWeight: 700,
              padding: '8px 18px', borderRadius: 8, cursor: 'pointer',
            }}>S'inscrire</button>
          </div>
        )}
      </div>
    </nav>
  );
};

// ── Car Card ──────────────────────────────────────────────────────────────────
export const CarCard = ({ car, seller, onClick, isFavorite, onToggleFavorite, premiumEnabled = false }) => {
  const [hovered, setHovered] = React.useState(false);

  const cardImage = car.primary_image_url
    || car.car_images?.find(i => i.is_primary)?.url
    || car.car_images?.[0]?.url
    || car.image
    || null;

  return (
    <div
      onClick={onClick}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        background: C.surface, border: `1px solid ${hovered ? C.faint : C.border}`,
        borderRadius: 16, overflow: 'hidden', cursor: 'pointer',
        transition: 'border-color 0.2s, transform 0.2s',
        transform: hovered ? 'translateY(-2px)' : 'none',
      }}
    >
      {/* Image */}
      <div style={{
        height: 200, background: car.gradient || C.surface,
        position: 'relative', overflow: 'hidden',
      }}>
        {cardImage && (
          <img src={cardImage} alt={`${car.make} ${car.model}`}
            style={{ width: '100%', height: '100%', objectFit: 'cover' }}
          />
        )}
        <div style={{ position: 'absolute', inset: 0, background: 'linear-gradient(to top, rgba(9,9,11,0.6) 0%, transparent 60%)' }} />
        {/* Badge Premium vendeur — visible seulement si le mode premium est actif */}
        {premiumEnabled && seller?.is_premium && (
          <div style={{
            position: 'absolute', top: 12, left: 12,
            background: 'linear-gradient(135deg, rgba(201,169,110,0.95), rgba(180,140,70,0.95))',
            backdropFilter: 'blur(6px)',
            border: `1px solid ${C.gold}`,
            color: '#09090B',
            fontSize: 10, fontWeight: 800, padding: '4px 10px', borderRadius: 20,
            fontFamily: C.dm, letterSpacing: '0.08em', textTransform: 'uppercase',
            display: 'flex', alignItems: 'center', gap: 4,
          }}>⭐ PREMIUM</div>
        )}
        {!seller?.is_premium && car.badge && (
          <div style={{
            position: 'absolute', top: 12, left: 12,
            background: 'rgba(9,9,11,0.65)', backdropFilter: 'blur(6px)',
            border: `1px solid ${C.goldBorder}`, color: C.gold,
            fontSize: 11, fontWeight: 600, padding: '4px 10px', borderRadius: 20,
            fontFamily: C.dm, letterSpacing: '0.06em',
          }}>{car.badge}</div>
        )}
        <button
          onClick={e => { e.stopPropagation(); onToggleFavorite && onToggleFavorite(car.id); }}
          style={{
            position: 'absolute', top: 12, right: 12,
            background: 'rgba(9,9,11,0.6)', border: 'none',
            color: isFavorite ? '#e05c5c' : C.muted, fontSize: 16,
            width: 32, height: 32, borderRadius: '50%', cursor: 'pointer',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
          }}
        >{isFavorite ? '♥' : '♡'}</button>
      </div>

      {/* Body */}
      <div style={{ padding: '16px 18px 18px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 8 }}>
          <div>
            <div style={{ fontFamily: C.playfair, fontSize: 18, fontWeight: 700, color: C.text }}>
              {car.make} {car.model}
            </div>
            <div style={{ fontFamily: C.dm, fontSize: 13, color: C.muted, marginTop: 2 }}>
              {car.year} · {(car.mileage || 0).toLocaleString('fr-FR')} km
            </div>
          </div>
          <div style={{ fontFamily: C.playfair, fontSize: 15, fontWeight: 700, color: C.gold, flexShrink: 0, textAlign: 'right', whiteSpace: 'nowrap', marginLeft: 8 }}>
            {toCFA(car.price)}
          </div>
        </div>

        <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 12 }}>
          {[car.fuel, car.transmission].filter(Boolean).map(tag => (
            <span key={tag} style={{
              fontFamily: C.dm, fontSize: 11, color: C.subtle,
              background: '#18181b', border: `1px solid ${C.border}`,
              padding: '3px 8px', borderRadius: 6,
            }}>{tag}</span>
          ))}
        </div>

        {seller && (
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, paddingTop: 12, borderTop: `1px solid ${C.border2}` }}>
            <div style={{
              width: 28, height: 28, borderRadius: '50%', background: '#27272A',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontFamily: C.dm, fontSize: 10, fontWeight: 700, color: C.muted, flexShrink: 0,
            }}>{seller.avatar}</div>
            <div style={{ flex: 1, minWidth: 0 }}>
              <div style={{ fontFamily: C.dm, fontSize: 12, color: C.text, fontWeight: 500, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                {seller.name}
                {seller.is_verified && <span style={{ color: C.gold, marginLeft: 4 }}>✓</span>}
                {premiumEnabled && seller.is_premium && <span style={{ color: '#C9A96E', marginLeft: 6, fontSize: 10, fontWeight: 700, background: 'rgba(201,169,110,0.15)', padding: '1px 6px', borderRadius: 10, border: '1px solid rgba(201,169,110,0.3)' }}>⭐ Premium</span>}
              </div>
              <div style={{ fontFamily: C.dm, fontSize: 11, color: C.muted }}>
                ★ {seller.rating} · {seller.location}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

// ── Button ────────────────────────────────────────────────────────────────────
export const Btn = ({ children, onClick, variant = 'primary', disabled, style = {} }) => {
  const base = {
    fontFamily: C.dm, fontSize: 14, fontWeight: 700,
    padding: '12px 24px', borderRadius: 10, cursor: disabled ? 'not-allowed' : 'pointer',
    border: 'none', transition: 'opacity 0.2s', opacity: disabled ? 0.5 : 1,
    ...style,
  };
  const variants = {
    primary: { background: C.gold, color: C.bg },
    secondary: { background: 'transparent', border: `1px solid ${C.border}`, color: C.text },
    ghost: { background: 'transparent', color: C.muted },
  };
  return (
    <button onClick={!disabled ? onClick : undefined} style={{ ...base, ...variants[variant] }}>
      {children}
    </button>
  );
};

// ── Input ─────────────────────────────────────────────────────────────────────
export const Input = ({ label, error, ...props }) => (
  <div>
    {label && (
      <label style={{ fontFamily: C.dm, fontSize: 12, color: C.muted, display: 'block', marginBottom: 7, textTransform: 'uppercase', letterSpacing: '0.06em' }}>
        {label}
      </label>
    )}
    <input
      {...props}
      style={{
        width: '100%', background: '#111113',
        border: `1px solid ${error ? C.error : C.border}`,
        color: C.text, fontFamily: C.dm, fontSize: 14,
        padding: '13px 16px', borderRadius: 10, outline: 'none',
        boxSizing: 'border-box',
        ...props.style,
      }}
      onFocus={e => { e.target.style.borderColor = C.gold; props.onFocus?.(e); }}
      onBlur={e => { e.target.style.borderColor = error ? C.error : C.border; props.onBlur?.(e); }}
    />
    {error && <p style={{ fontFamily: C.dm, fontSize: 12, color: C.error, marginTop: 5 }}>{error}</p>}
  </div>
);

// ── Badge ─────────────────────────────────────────────────────────────────────
export const StatusBadge = ({ status }) => {
  const styles = {
    confirmed: { bg: 'rgba(34,197,94,0.1)', color: '#4ade80', border: 'rgba(34,197,94,0.3)', label: 'Confirmé' },
    pending:   { bg: 'rgba(234,179,8,0.1)',  color: '#facc15', border: 'rgba(234,179,8,0.3)',  label: 'En attente' },
    cancelled: { bg: 'rgba(239,68,68,0.1)',  color: '#f87171', border: 'rgba(239,68,68,0.3)',  label: 'Annulé' },
    completed: { bg: 'rgba(99,102,241,0.1)', color: '#818cf8', border: 'rgba(99,102,241,0.3)', label: 'Terminé' },
  };
  const s = styles[status] || styles.pending;
  return (
    <span style={{
      fontFamily: C.dm, fontSize: 11, fontWeight: 600,
      background: s.bg, color: s.color, border: `1px solid ${s.border}`,
      padding: '3px 10px', borderRadius: 20, letterSpacing: '0.04em',
    }}>{s.label}</span>
  );
};

// ── Loading ───────────────────────────────────────────────────────────────────
export const Spinner = () => (
  <div style={{ display: 'flex', justifyContent: 'center', padding: '80px 0' }}>
    <div style={{
      width: 36, height: 36, border: `3px solid ${C.border}`,
      borderTopColor: C.gold, borderRadius: '50%',
      animation: 'spin 0.8s linear infinite',
    }} />
    <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
  </div>
);
