export enum Area {
  Tier1 = 'Tier1',
  Tier2 = 'Tier2',
  Tier3 = 'Tier3',
}

export type AreaRect = {
  x: number;
  y: number;
  width: number;
  height: number;
};

export type AreaMeta = {
  rect: AreaRect;
  backgroundColor?: string; // 将来的には backgroundImage でもOK
  backgroundImage?: string;
};

export const areaMap: Record<Area, AreaMeta> = {
  [Area.Tier1]: {
    rect: { x: 0, y: 0, width: 512, height: 300 },
    backgroundImage: '/Tier/Tier1.png',
  },
  [Area.Tier2]: {
    rect: { x: 512, y: 0, width: 512, height: 300 },
    backgroundImage: '/Tier/Tier2.png',
  },
  [Area.Tier3]: {
    rect: { x: 0, y: 310, width: 1024, height: 300 },
    backgroundImage: '/Tier/Tier3.png',
  },
};

export const getAreaRect = (area: Area): AreaRect => areaMap[area].rect;

export const getAreaStyle = (area: Area): React.CSSProperties => {
  const meta = areaMap[area];
  return {
    // backgroundColor: meta.backgroundColor,
    backgroundImage: meta.backgroundImage ? `url(${meta.backgroundImage})` : undefined,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
  };
};

/**
 * (x,y) をスプライト左上としたとき、
 * spriteMargin×spriteMargin のスプライトが
 * 完全に area の中に収まるか判定する
 */
export const isInArea = (
  x: number,
  y: number,
  area: Area,
  spriteMargin: number = 50
): boolean => {
  const rect: AreaRect = getAreaRect(area);
  // 左上が左端／上端より下かつ
  // 右下 (x+margin, y+margin) が右端／下端より上か
  return (
    x >= rect.x &&
    y >= rect.y &&
    x + spriteMargin <= rect.x + rect.width &&
    y + spriteMargin <= rect.y + rect.height
  );
};

export const getAreaByPosition = (x: number, y: number): Area | null => {
  return (Object.entries(areaMap) as [Area, AreaMeta][])  // ✅ ここを修正！
    .find(([area, _]) => isInArea(x, y, area))?.[0] ?? null;
};


/**
 * area 内に spriteMargin×spriteMargin のスプライトが
 * 完全に収まる乱数位置を返す
 */
export const getRandomPositionInArea = (
  area: Area,
  spriteMargin: number = 50
): { x: number; y: number } => {
  const { x: rx, y: ry, width, height } = getAreaRect(area);
  console.log("rect:", getAreaRect(area))
  // スプライトがはみ出さないように、乱数の上限を (領域幅 - マージン) に調整
  const maxX = rx + width  - spriteMargin;
  const maxY = ry + height - spriteMargin;

  // min は領域の左上（rx, ry）
  const minX = rx;
  const minY = ry;

  // 乱数生成
  const x = Math.floor(minX + Math.random() * (maxX - minX));
  const y = Math.floor(minY + Math.random() * (maxY - minY));
  console.log("init:", x, y)
  return { x, y };
};

// 📐 全体フィールドの最大サイズ（自動算出）
export const fieldWidth = Math.max(...Object.values(areaMap).map(a => a.rect.x + a.rect.width));
export const fieldHeight = Math.max(...Object.values(areaMap).map(a => a.rect.y + a.rect.height));
