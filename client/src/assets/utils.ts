import checkmarkSVG from 'assets/checkmark.svg';
import copySVG from 'assets/copy.svg';
import discordSVG from 'assets/discord.svg';
import downloadSVG from 'assets/download.svg';
import githubSVG from 'assets/github.svg';
import helpSVG from 'assets/help.svg';
import infoSVG from 'assets/info.svg';
import logoSVG from 'assets/logo.svg';
import playSVG from 'assets/play.svg';
import twitterSVG from 'assets/twitter.svg';

export function renderIcon(name: string) {
  const icon: { [key: string]: { src: string } } = {
    checkmark: checkmarkSVG,
    copy: copySVG,
    discord: discordSVG,
    download: downloadSVG,
    github: githubSVG,
    help: helpSVG,
    info: infoSVG,
    logo: logoSVG,
    play: playSVG,
    twitter: twitterSVG,
  };

  return icon[name].src;
}
