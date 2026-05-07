import React from 'react';
import { C, Logo, Input } from './Shared';
import { authApi } from '../api';

// ── Helpers de validation ────────────────────────────────────────────────────
const PHONE_RE = /^(\+?221)?\s?(7[05678])\s?\d{3}\s?\d{2}\s?\d{2}$/;
const CNI_RE = /^\d{13}$/;
const cleanDigits = (v) => (v || '').replace(/\s+/g, '');

// ── Indicateur de solidité du mot de passe ───────────────────────────────────
function passwordStrength(pwd) {
  if (!pwd) return 0;
  let score = 0;
  if (pwd.length >= 6) score++;
  if (pwd.length >= 10) score++;
  if (/[A-Z]/.test(pwd) && /[a-z]/.test(pwd)) score++;
  if (/\d/.test(pwd) && /[^A-Za-z0-9]/.test(pwd)) score++;
  return Math.min(score, 4);
}

const STRENGTH_LABELS = ['', 'Faible', 'Moyen', 'Bon', 'Fort'];
const STRENGTH_COLORS = ['', '#e05c5c', '#e08a3c', '#d4c043', '#4caf7d'];

function PasswordStrengthBar({ password }) {
  const s = passwordStrength(password);
  if (!password) return null;
  return (
    <div style={{ marginTop: 8 }}>
      <div style={{ display: 'flex', gap: 5, marginBottom: 5 }}>
        {[1, 2, 3, 4].map(i => (
          <div key={i} style={{
            flex: 1, height: 4, borderRadius: 4,
            background: i <= s ? STRENGTH_COLORS[s] : '#27272A',
            transition: 'background 0.3s',
          }} />
        ))}
      </div>
      <span style={{ fontFamily: C.dm, fontSize: 11, color: STRENGTH_COLORS[s] }}>
        {STRENGTH_LABELS[s]}
      </span>
    </div>
  );
}

function PasswordInput({ label, value, onChange, placeholder, error, show, onToggle }) {
  const [focused, setFocused] = React.useState(false);
  return (
    <div>
      {label && (
        <label style={{ fontFamily: C.dm, fontSize: 12, color: C.muted, display: 'block', marginBottom: 7, textTransform: 'uppercase', letterSpacing: '0.06em' }}>
          {label}
        </label>
      )}
      <div style={{ position: 'relative' }}>
        <input
          type={show ? 'text' : 'password'}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          style={{
            width: '100%', background: '#111113',
            border: `1px solid ${error ? C.error : focused ? C.gold : C.border}`,
            color: C.text, fontFamily: C.dm, fontSize: 14,
            padding: '13px 46px 13px 16px', borderRadius: 10, outline: 'none',
            boxSizing: 'border-box', transition: 'border-color 0.15s',
          }}
          onFocus={() => setFocused(true)}
          onBlur={() => setFocused(false)}
        />
        <button
          type="button"
          onClick={onToggle}
          style={{
            position: 'absolute', right: 12, top: '50%', transform: 'translateY(-50%)',
            background: 'none', border: 'none', cursor: 'pointer',
            color: show ? C.gold : C.muted, fontSize: 17, padding: 4,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            transition: 'color 0.15s',
          }}
          tabIndex={-1}
          title={show ? 'Masquer le mot de passe' : 'Afficher le mot de passe'}
        >
          {show ? (
            // Œil barré
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94" />
              <path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19" />
              <line x1="1" y1="1" x2="23" y2="23" />
            </svg>
          ) : (
            // Œil ouvert
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
              <circle cx="12" cy="12" r="3" />
            </svg>
          )}
        </button>
      </div>
      {error && <p style={{ fontFamily: C.dm, fontSize: 12, color: C.error, marginTop: 5 }}>{error}</p>}
    </div>
  );
}

// ── Modale de compte bloqué ───────────────────────────────────────────────────
function BlockedModal({ info, onClose }) {
  const isBanned = info.account_status === 'banned';

  const formatDate = (iso) => {
    if (!iso) return null;
    return new Date(iso).toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric' });
  };

  return (
    <div style={{
      position: 'fixed', inset: 0, zIndex: 999,
      background: 'rgba(0,0,0,0.85)', backdropFilter: 'blur(12px)',
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      padding: '24px',
    }}>
      <div style={{
        background: C.surface, border: `1px solid ${isBanned ? 'rgba(239,68,68,0.4)' : 'rgba(234,179,8,0.4)'}`,
        borderRadius: 24, padding: '40px 36px', maxWidth: 480, width: '100%',
        boxShadow: `0 0 60px ${isBanned ? 'rgba(239,68,68,0.15)' : 'rgba(234,179,8,0.1)'}`,
      }}>
        {/* Icône */}
        <div style={{
          width: 72, height: 72, borderRadius: '50%', margin: '0 auto 24px',
          background: isBanned ? 'rgba(239,68,68,0.12)' : 'rgba(234,179,8,0.12)',
          border: `2px solid ${isBanned ? 'rgba(239,68,68,0.4)' : 'rgba(234,179,8,0.4)'}`,
          display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 32,
        }}>
          {isBanned ? '🚫' : '⏸️'}
        </div>

        {/* Titre */}
        <h2 style={{
          fontFamily: C.playfair, fontSize: 26, fontWeight: 700,
          color: isBanned ? '#f87171' : '#facc15',
          textAlign: 'center', margin: '0 0 8px',
        }}>
          {isBanned ? 'Compte banni' : 'Compte suspendu'}
        </h2>

        {/* Sous-titre */}
        <p style={{ fontFamily: C.dm, fontSize: 14, color: C.muted, textAlign: 'center', margin: '0 0 24px' }}>
          {isBanned
            ? "Votre accès à AutoConnect a été définitivement révoqué par l'administration."
            : "Votre compte a été temporairement suspendu par l'administration."}
        </p>

        {/* Note admin */}
        {info.reason ? (
          <div style={{
            background: isBanned ? 'rgba(239,68,68,0.07)' : 'rgba(234,179,8,0.07)',
            border: `1px solid ${isBanned ? 'rgba(239,68,68,0.25)' : 'rgba(234,179,8,0.25)'}`,
            borderRadius: 12, padding: '16px 18px', marginBottom: 20,
          }}>
            <div style={{ fontFamily: C.dm, fontSize: 11, color: C.muted, textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: 8 }}>
              Motif communiqué par l'administration
            </div>
            <div style={{ fontFamily: C.dm, fontSize: 14, color: C.text, lineHeight: 1.6 }}>
              "{info.reason}"
            </div>
          </div>
        ) : (
          <div style={{
            background: 'rgba(113,113,122,0.08)', border: `1px solid ${C.border}`,
            borderRadius: 12, padding: '14px 18px', marginBottom: 20,
          }}>
            <div style={{ fontFamily: C.dm, fontSize: 13, color: C.muted, fontStyle: 'italic' }}>
              Aucun motif précisé par l'administration.
            </div>
          </div>
        )}

        {/* Date de fin (ban ou suspension avec durée) */}
        {info.ban_until && (
          <div style={{ fontFamily: C.dm, fontSize: 13, color: C.muted, textAlign: 'center', marginBottom: 20 }}>
            {isBanned ? 'Banni' : 'Suspendu'} jusqu'au{' '}
            <strong style={{ color: isBanned ? '#f87171' : '#facc15' }}>{formatDate(info.ban_until)}</strong>
          </div>
        )}

        {/* Bouton retour */}
        <button onClick={onClose} style={{
          width: '100%', padding: '14px',
          background: isBanned ? 'rgba(239,68,68,0.12)' : 'rgba(234,179,8,0.12)',
          border: `1px solid ${isBanned ? 'rgba(239,68,68,0.35)' : 'rgba(234,179,8,0.35)'}`,
          color: isBanned ? '#f87171' : '#facc15',
          fontFamily: C.dm, fontSize: 14, fontWeight: 700,
          borderRadius: 12, cursor: 'pointer',
        }}>
          Retourner à l'accueil
        </button>
      </div>
    </div>
  );
}

export default function Auth({ navigate, setUser, initialMode, initialType }) {
  const [mode, setMode] = React.useState(initialMode || 'login');
  const [accountType, setAccountType] = React.useState(initialType || 'buyer');
  const [form, setForm] = React.useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    company: '',
    phone: '',
    id_card_number: '',
  });
  const [errors, setErrors] = React.useState({});
  const [loading, setLoading] = React.useState(false);
  const [apiError, setApiError] = React.useState('');
  const [showPassword, setShowPassword] = React.useState(false);
  const [showConfirm, setShowConfirm] = React.useState(false);
  const [blockedInfo, setBlockedInfo] = React.useState(null);

  const setField = (k, v) => {
    setForm(f => ({ ...f, [k]: v }));
    if (errors[k]) setErrors(e => ({ ...e, [k]: undefined }));
  };

  const validate = () => {
    const e = {};
    if (!form.email.includes('@')) e.email = 'Email invalide';
    if (form.password.length < 6) e.password = 'Min. 6 caractères';

    if (mode === 'register') {
      if (form.confirmPassword !== form.password) e.confirmPassword = 'Les mots de passe ne correspondent pas';
      if (!form.name.trim()) e.name = 'Requis';
      const phoneClean = cleanDigits(form.phone);
      if (!phoneClean) e.phone = 'Téléphone requis';
      else if (!PHONE_RE.test(phoneClean)) e.phone = 'Numéro sénégalais invalide (ex: 77 123 45 67)';

      const cniClean = cleanDigits(form.id_card_number);
      if (!cniClean) e.id_card_number = 'CNI requise';
      else if (!CNI_RE.test(cniClean)) e.id_card_number = 'La CNI doit avoir 13 chiffres';
    }
    return e;
  };

  const handleSubmit = async () => {
    const e = validate();
    if (Object.keys(e).length) { setErrors(e); return; }
    setLoading(true);
    setApiError('');
    try {
      let res;
      if (mode === 'login') {
        res = await authApi.login({ email: form.email.trim(), password: form.password });
      } else {
        const [firstName, ...rest] = form.name.trim().split(' ');
        res = await authApi.register({
          email: form.email.trim(),
          password: form.password,
          first_name: firstName,
          last_name: rest.join(' ') || firstName,
          user_type: accountType,
          company: form.company,
          phone: cleanDigits(form.phone),
          id_card_number: cleanDigits(form.id_card_number),
        });
      }
      localStorage.setItem('access_token', res.data.access);
      localStorage.setItem('refresh_token', res.data.refresh);
      setUser(res.data.user);
      navigate(
        res.data.user.user_type === 'seller' ? 'seller-dashboard' :
        res.data.user.user_type === 'admin'  ? 'admin-dashboard'  : 'buyer-dashboard'
      );
    } catch (err) {
      const data = err.response?.data;
      // Compte banni ou suspendu → modale dédiée
      if (err.response?.status === 403 && data?.account_status) {
        setBlockedInfo(data);
        return;
      }
      if (typeof data === 'string') setApiError(data);
      else if (data?.non_field_errors) setApiError(data.non_field_errors[0]);
      else if (data?.email) setApiError(`Email : ${data.email[0]}`);
      else if (data?.phone) setApiError(`Téléphone : ${data.phone[0]}`);
      else if (data?.id_card_number) setApiError(`CNI : ${data.id_card_number[0]}`);
      else if (data?.password) setApiError(`Mot de passe : ${data.password[0]}`);
      else if (data?.detail) setApiError(data.detail);
      else setApiError('Une erreur est survenue. Réessayez.');
    } finally {
      setLoading(false);
    }
  };

  // Permet d'envoyer le formulaire avec Entree
  const onKeyDown = (e) => { if (e.key === 'Enter' && !loading) handleSubmit(); };

  return (
    <div style={{ minHeight: '100vh', background: C.bg, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '80px 24px' }}>
      {blockedInfo && <BlockedModal info={blockedInfo} onClose={() => navigate('home')} />}
      <div style={{ width: '100%', maxWidth: 480 }}>
        <div style={{ textAlign: 'center', marginBottom: 40 }}>
          <Logo size="lg" onClick={() => navigate('home')} />
        </div>

        <div style={{ background: C.surface, border: `1px solid ${C.border}`, borderRadius: 24, padding: 40 }}>
          {/* Toggle */}
          <div style={{ display: 'flex', background: '#0e0e10', borderRadius: 12, padding: 4, marginBottom: 32 }}>
            {[['login', 'Connexion'], ['register', 'Créer un compte']].map(([m, label]) => (
              <button key={m} onClick={() => { setMode(m); setErrors({}); setApiError(''); }} style={{
                flex: 1, padding: '10px', borderRadius: 10, border: 'none',
                background: mode === m ? '#1e1e21' : 'transparent',
                color: mode === m ? C.text : C.muted,
                fontFamily: C.dm, fontSize: 14, fontWeight: mode === m ? 600 : 400,
                cursor: 'pointer',
              }}>{label}</button>
            ))}
          </div>

          {/* Account type (register only) */}
          {mode === 'register' && (
            <div style={{ marginBottom: 28 }}>
              <label style={{ fontFamily: C.dm, fontSize: 12, color: C.muted, display: 'block', marginBottom: 8, textTransform: 'uppercase', letterSpacing: '0.06em' }}>Je suis</label>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
                {[['buyer', '🛒', 'Acheteur', 'Je cherche un véhicule'], ['seller', '🏷', 'Vendeur', 'Je publie des annonces']].map(([type, icon, title, sub]) => (
                  <button key={type} onClick={() => setAccountType(type)} style={{
                    background: accountType === type ? 'rgba(201,169,110,0.08)' : 'transparent',
                    border: `1px solid ${accountType === type ? C.goldBorder : C.border}`,
                    borderRadius: 12, padding: '16px', cursor: 'pointer', textAlign: 'left',
                  }}>
                    <div style={{ fontSize: 22, marginBottom: 6 }}>{icon}</div>
                    <div style={{ fontFamily: C.dm, fontSize: 14, fontWeight: 600, color: accountType === type ? C.gold : C.text, marginBottom: 3 }}>{title}</div>
                    <div style={{ fontFamily: C.dm, fontSize: 11, color: C.subtle }}>{sub}</div>
                  </button>
                ))}
              </div>
            </div>
          )}

          {apiError && (
            <div style={{
              background: 'rgba(224,92,92,0.1)', border: '1px solid rgba(224,92,92,0.3)',
              borderRadius: 10, padding: '12px 16px', marginBottom: 20,
              fontFamily: C.dm, fontSize: 13, color: C.error,
            }}>{apiError}</div>
          )}

          <div style={{ display: 'flex', flexDirection: 'column', gap: 18 }} onKeyDown={onKeyDown}>
            {mode === 'register' && (
              <Input
                label={accountType === 'seller' ? 'Nom / Enseigne' : 'Prénom et nom'}
                value={form.name}
                onChange={e => setField('name', e.target.value)}
                placeholder={accountType === 'seller' ? 'Premium Motors Dakar' : 'Jean Dupont'}
                error={errors.name}
              />
            )}

            <Input
              label="Adresse email"
              type="email"
              value={form.email}
              onChange={e => setField('email', e.target.value)}
              placeholder="votre@email.com"
              error={errors.email}
            />

            {mode === 'register' && (
              <>
                <Input
                  label="Téléphone"
                  type="tel"
                  value={form.phone}
                  onChange={e => setField('phone', e.target.value)}
                  placeholder="+221 77 123 45 67"
                  error={errors.phone}
                />

                <Input
                  label="Numéro de carte d'identité (CNI)"
                  type="text"
                  value={form.id_card_number}
                  onChange={e => setField('id_card_number', e.target.value.replace(/\D/g, '').slice(0, 13))}
                  placeholder="13 chiffres"
                  error={errors.id_card_number}
                />
              </>
            )}

            <div>
              <PasswordInput
                label="Mot de passe"
                value={form.password}
                onChange={e => setField('password', e.target.value)}
                placeholder="••••••••"
                error={errors.password}
                show={showPassword}
                onToggle={() => setShowPassword(v => !v)}
              />
              {mode === 'register' && <PasswordStrengthBar password={form.password} />}
            </div>

            {mode === 'register' && (
              <PasswordInput
                label="Confirmer le mot de passe"
                value={form.confirmPassword}
                onChange={e => setField('confirmPassword', e.target.value)}
                placeholder="••••••••"
                error={errors.confirmPassword}
                show={showConfirm}
                onToggle={() => setShowConfirm(v => !v)}
              />
            )}

            <button onClick={handleSubmit} disabled={loading} style={{
              background: loading ? 'rgba(201,169,110,0.5)' : C.gold,
              border: 'none', color: C.bg, fontFamily: C.dm,
              fontSize: 15, fontWeight: 700, padding: '14px', borderRadius: 10,
              cursor: loading ? 'not-allowed' : 'pointer', marginTop: 8,
            }}>
              {loading ? 'Veuillez patienter...' : mode === 'login' ? 'Se connecter' : 'Créer mon compte'}
            </button>
          </div>

          <p style={{ fontFamily: C.dm, fontSize: 13, color: C.subtle, textAlign: 'center', margin: '24px 0 0' }}>
            {mode === 'login' ? "Pas encore de compte ? " : "Déjà un compte ? "}
            <span onClick={() => { setMode(mode === 'login' ? 'register' : 'login'); setErrors({}); setApiError(''); }}
              style={{ color: C.gold, cursor: 'pointer', fontWeight: 600 }}>
              {mode === 'login' ? "S'inscrire" : "Se connecter"}
            </span>
          </p>
        </div>
      </div>
    </div>
  );
}
