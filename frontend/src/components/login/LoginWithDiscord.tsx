import React from 'react';
import TypewriterText from '../ui/TypewriterText';

interface LoginWithDiscordProps {
  message?: {
    type: 'success' | 'error' | 'info';
    message: string;
  } | null;
  onClearMessage?: () => void;
}

const LoginWithDiscord: React.FC<LoginWithDiscordProps> = ({ message, onClearMessage }) => {
    const handleLogin = () => {
        const clientId = import.meta.env.VITE_DISCORD_CLIENT_ID;
        const redirectUri = import.meta.env.VITE_DISCORD_REDIRECT_URI;
        const scope = import.meta.env.VITE_DISCORD_SCOPE;
        const discordAuthUrl = `https://discord.com/oauth2/authorize?client_id=${clientId}&response_type=code&redirect_uri=${encodeURIComponent(redirectUri)}&scope=${encodeURIComponent(scope)}`;

        window.location.href = discordAuthUrl;
        console.log('Redirecting to Discord for login...');
    };

    return (
        <>
        <div className="login-requirement">
            <h2>Terminal Requirments:</h2>
            <p>
                Must have a Discord account.<br />
                Must be registered with the server.<br />
                Terminal priveledges are dependent upon approval.
            </p>
        </div>
        <div className="message-response">
            {message && (
                <h2>
                    <TypewriterText 
                        text={message.message}
                        speed={35}
                        cursorBlinkRate={500}
                        cursorChar="_"
                    />
                </h2>
            )}
        </div>
        <div className="discord-login">
            <button onClick={handleLogin}>
                Login with Discord
            </button>
        </div>
        </>
    );
}

export default LoginWithDiscord;