import { Direction } from '../domain/user/Direction';

type Props = {
  direction: Direction;
  isWalking: boolean;
};

const DIRECTION_ROW_MAP: Record<Direction, number> = {
  down: 0,
  left: 1,
  right: 2,
  up: 3,
};

export const Sprite = ({ direction, isWalking }: Props) => {
  const spriteSize = 32;
  const row = DIRECTION_ROW_MAP[direction];
  
  return (
    <div
      className={`sprite ${isWalking ? 'walking' : ''}`}
      style={{
        backgroundImage: `url('/icons/pipo-charachip014a.png')`,
        width: `${spriteSize}px`,
        height: `${spriteSize}px`,
        backgroundPosition: `0px -${row * spriteSize}px`,
        animation: isWalking ? `walk-${direction} 0.6s steps(3) infinite` : undefined,
      }}
    />
  );
};
