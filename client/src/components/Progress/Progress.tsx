import { ReactNode } from 'react';
import styles from './styles.module.css';

function Progress({ width, children }: { width: number; children: ReactNode }) {
  return (
    <div className={styles.progressBar}>
      <div className={styles.progressBarIndicator} style={{ maxWidth: `calc(${width}% - 0.4rem)` }} />
      {children}
    </div>
  );
}

export default Progress;
