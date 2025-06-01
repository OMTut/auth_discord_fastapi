import React from 'react';

const LoginWithDiscord: React.FC = () => {
    const handleLogin = () => {
        const clientId = import.meta.env.VITE_DISCORD_CLIENT_ID;
        const redirectUri = import.meta.env.VITE_DISCORD_REDIRECT_URI;
        const scope = 'identify email';
        const discordAuthUrl = `https://discord.com/api/oauth2/authorize?client_id=${clientId}&redirect_uri=${encodeURIComponent(redirectUri)}&response_type=code&scope=${encodeURIComponent(scope)}`;

        window.location.href = discordAuthUrl;
        console.log('Redirecting to Discord for login...');
    };

    return (
        <div className="discord-login">
            <button onClick={handleLogin}>
                Login with Discord
            </button>
        </div>
    );
}

export default LoginWithDiscord;