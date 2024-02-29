/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.tsx'],
  theme: {
    colors: {
      white: '#ffffff',
      blue: '#181ea9',
      black: '#000000',
      ghost: '#f6f8fc',
      grey: '#cfcfcf',
      stone: '#9c9c9c',
      transparent: 'transparent',
    },
    fontFamily: {
      sans: ['Inter', 'sans'],
      mono: ['Roboto Mono', 'mono'],
    },
    fontSize: {
      9: [
        '0.9rem',
        {
          lineHeight: '2.4rem',
          letterSpacing: '0.028rem',
          fontWeight: '500',
        },
      ],
      10: [
        '1rem',
        {
          lineHeight: '1.3rem',
          letterSpacing: '0.007rem',
          fontWeight: '700',
        },
      ],
      12: [
        '1.2rem',
        {
          lineHeight: '1.6rem',
          letterSpacing: '0.009rem',
          fontWeight: '500',
        },
      ],
      14: [
        '1.4rem',
        {
          lineHeight: '1.9rem',
          letterSpacing: '0.044rem',
          fontWeight: '500',
        },
      ],
      16: [
        '1.6rem',
        {
          lineHeight: '1.8rem',
          letterSpacing: '0.05rem',
          fontWeight: '700',
        },
      ],
      18: [
        '1.8rem',
        {
          lineHeight: '2.4rem',
          letterSpacing: '0.001rem',
          fontWeight: '500',
        },
      ],
      24: [
        '2.4rem',
        {
          lineHeight: '3.1rem',
          letterSpacing: '0.025rem',
          fontWeight: '700',
        },
      ],
      34: [
        '3.4rem',
        {
          lineHeight: '4.1rem',
          letterSpacing: '0.025rem',
          fontWeight: '700',
        },
      ],
    },
    container: {
      center: true,
    },
    extend: {
      spacing: {
        '8xl': '96rem',
        '9xl': '128rem',
      },
      borderRadius: {
        '4xl': '2rem',
      },
    },
  },
  plugins: [],
};
