(function() {
    // 1. Override fetch IMMEDIATELY to catch any early requests
    const originalFetch = window.fetch;
    window.fetch = async function() {
        let [resource, config] = arguments;
        if (typeof resource === 'string' && resource.startsWith('/api/') && !resource.startsWith('/api/auth')) {
            config = config || {};
            config.headers = config.headers || {};
            const token = sessionStorage.getItem('authToken') || localStorage.getItem('authToken');
            if (token) {
                config.headers['Authorization'] = `Bearer ${token}`;
            }
        }
        
        const response = await originalFetch(resource, config);
        
        if (response.status === 401) {
            // Clone the response because reading body consumes it
            const clonedResponse = response.clone();
            const data = await clonedResponse.json().catch(()=>({}));
            
            if (data.code === 'FIRST_RUN') {
                showAuthModal('register', true);
            } else {
                showAuthModal('login');
            }
            // Return the original response so calling code can handle the status
            return response;
        }
        return response;
    };

    function revealUI() {
        document.querySelectorAll('.auth-gated').forEach(el => {
            el.classList.add('auth-visible');
        });
    }

    function showAuthModal(mode, isFirstRunLocal = false) {
        ensureModalInjected();
        const authModal = document.getElementById('auth-modal');
        const authTitle = document.getElementById('auth-title');
        const authSubmitBtn = document.getElementById('auth-submit-btn');
        
        authModal.style.display = 'flex';
        authModal.classList.add('visible');
        
        if (mode === 'register' || isFirstRunLocal) {
            authTitle.textContent = 'Register New User (First Run)';
            authSubmitBtn.textContent = 'Register';
        } else {
            authTitle.textContent = 'Login';
            authSubmitBtn.textContent = 'Login';
        }
    }

    function ensureModalInjected() {
        if (!document.getElementById('auth-modal')) {
            const modalHtml = `
            <div id="auth-modal" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.9); display: none; align-items: center; justify-content: center; z-index: 2000; font-family: sans-serif;">
                <div class="modal-content" style="max-width: 400px; width: 100%; padding: 30px; background: #2C2C32; border: 1px solid #9F7AEA; border-radius: 8px; color: white;">
                    <h2 id="auth-title" style="margin-top: 0; text-align: center; color: #9F7AEA;">Login</h2>
                    <form id="auth-form">
                        <div class="form-group" style="margin-bottom: 15px;">
                            <label style="display: block; margin-bottom: 5px;">Username</label>
                            <input type="text" id="auth-username" class="form-control" style="width: 100%; padding: 10px; background: #1A1A1E; color: white; border: 1px solid #444; border-radius: 4px;" required>
                        </div>
                        <div class="form-group" style="margin-bottom: 15px;">
                            <label style="display: block; margin-bottom: 5px;">Password</label>
                            <input type="password" id="auth-password" class="form-control" style="width: 100%; padding: 10px; background: #1A1A1E; color: white; border: 1px solid #444; border-radius: 4px;" required>
                        </div>
                        <div class="form-group" style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
                            <input type="checkbox" id="auth-remember" ${localStorage.getItem('rememberUser') === 'true' ? 'checked' : ''}>
                            <label for="auth-remember" style="margin: 0; cursor: pointer;">Remember me</label>
                        </div>
                        <button type="submit" class="btn" style="width: 100%; margin-top: 15px; background: #9F7AEA; color: white; border: none; padding: 12px; border-radius: 8px; cursor: pointer; font-weight: bold;" id="auth-submit-btn">Login</button>
                        <div id="auth-feedback" class="feedback" style="margin-top: 15px; text-align: center; display: none; font-size: 0.9em;"></div>
                    </form>
                </div>
            </div>
            `;
            document.body.insertAdjacentHTML('beforeend', modalHtml);
            
            document.getElementById('auth-form').addEventListener('submit', async (e) => {
                e.preventDefault();
                const username = document.getElementById('auth-username').value;
                const password = document.getElementById('auth-password').value;
                const remember = document.getElementById('auth-remember').checked;
                const feedback = document.getElementById('auth-feedback');
                
                const isRegister = document.getElementById('auth-title').textContent.includes('Register');
                const mode = isRegister ? 'register' : 'login';

                feedback.style.display = 'block';
                feedback.style.color = 'white';
                feedback.textContent = 'Please wait...';

                try {
                    const res = await originalFetch(`/api/auth/${mode}`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ username, password })
                    });
                    const data = await res.json();
                    if (!res.ok) throw new Error(data.error);

                    if (remember) {
                        localStorage.setItem('authToken', data.token);
                        localStorage.setItem('rememberUser', 'true');
                    } else {
                        sessionStorage.setItem('authToken', data.token);
                        localStorage.removeItem('authToken'); // Make sure we don't have conflicts with old tokens
                        localStorage.removeItem('rememberUser');
                    }

                    document.getElementById('auth-modal').style.display = 'none';
                    location.reload(); 
                } catch (e) {
                    feedback.style.color = '#ff6b6b';
                    feedback.textContent = e.message;
                }
            });
        }
    }

    // Check status on load
    document.addEventListener('DOMContentLoaded', () => {
        ensureModalInjected();
        
        originalFetch('/api/auth/status').then(res => res.json()).then(data => {
            if (!data.hasUsers) {
                showAuthModal('register', true);
            } else {
                const token = sessionStorage.getItem('authToken') || localStorage.getItem('authToken');
                if (!token) {
                    showAuthModal('login');
                } else {
                    revealUI();
                }
            }
        }).catch(err => {
            console.error("Auth status check failed", err);
        });
    });

    // Handle logout
    window.logoutUser = () => {
        originalFetch('/api/auth/logout', { method: 'POST' }).catch(() => {});
        localStorage.removeItem('authToken');
        localStorage.removeItem('rememberUser');
        sessionStorage.removeItem('authToken');
        console.log("[AUTH] Logout executed, tokens and preferences removed.");
        location.reload();
    };
})();
