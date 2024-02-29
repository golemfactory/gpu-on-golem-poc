import backSVG from 'assets/back.svg';
import checkmarkSVG from 'assets/checkmark.svg';
import clearSVG from 'assets/clear.svg';
import copySVG from 'assets/copy.svg';
import discordWhiteSVG from 'assets/discord-white.svg';
import discordSVG from 'assets/discord.svg';
import downloadStoneSVG from 'assets/download-stone.svg';
import downloadSVG from 'assets/download.svg';
import githubSVG from 'assets/github.svg';
import helpSVG from 'assets/help.svg';
import infoSVG from 'assets/info.svg';
import logoSVG from 'assets/logo.svg';
import playBlackSVG from 'assets/play-black.svg';
import playSVG from 'assets/play.svg';
import twitterSVG from 'assets/twitter.svg';

export function renderIcon(name: string) {
  const icon: { [key: string]: { src: string } } = {
    back: backSVG,
    checkmark: checkmarkSVG,
    clear: clearSVG,
    copy: copySVG,
    discordWhite: discordWhiteSVG,
    discord: discordSVG,
    downloadStone: downloadStoneSVG,
    download: downloadSVG,
    github: githubSVG,
    help: helpSVG,
    info: infoSVG,
    logo: logoSVG,
    playBlack: playBlackSVG,
    play: playSVG,
    twitter: twitterSVG,
  };

  return icon[name].src;
}
