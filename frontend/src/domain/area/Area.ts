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
 * (x, y) は「エリア左上を (0,0) とした相対座標」
 * spriteMargin × spriteMargin のスプライトが
 * 完全に area 内に収まるか返す
 */
export const isInArea = (
  x: number,
  y: number,
  area: Area,
  spriteMargin: number = 50
): boolean => {
  const { width, height } = getAreaRect(area);
  return (
    x >= 0 &&
    y >= 0 &&
    x + spriteMargin <= width &&
    y + spriteMargin <= height
  );
};

export const getAreaByPosition = (x: number, y: number): Area | null => {
  return (Object.entries(areaMap) as [Area, AreaMeta][])
    .find(([area, _]) => isInArea(x, y, area))?.[0] ?? null;
};


/** 
 * area 内に spriteMargin(=50)のマージンを見て
 * 相対座標でランダム位置を返す (0 <= x <= width - margin)
 */
export const getRandomPositionInArea = (
  area: Area,
  spriteMargin: number = 50
): { x: number; y: number } => {
  const { width, height } = getAreaRect(area);

  const maxX = width  - spriteMargin;
  const maxY = height - spriteMargin;

  return {
    x: Math.floor(Math.random() * maxX),  // すでに相対
    y: Math.floor(Math.random() * maxY),
  };
};

// 📐 全体フィールドの最大サイズ（自動算出）
export const fieldWidth = Math.max(...Object.values(areaMap).map(a => a.rect.x + a.rect.width));
export const fieldHeight = Math.max(...Object.values(areaMap).map(a => a.rect.y + a.rect.height));
