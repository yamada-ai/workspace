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
};

export const areaMap: Record<Area, AreaMeta> = {
  [Area.Tier1]: {
    rect: { x: 0, y: 0, width: 320, height: 256 },
    backgroundColor: '#e0f7fa', // 薄い水色
  },
  [Area.Tier2]: {
    rect: { x: 360, y: 64, width: 320, height: 256 },
    backgroundColor: '#f1f8e9', // 薄い緑
  },
  [Area.Tier3]: {
    rect: { x: 160, y: 340, width: 320, height: 192 },
    backgroundColor: '#fff3e0', // 薄いオレンジ
  },
};

export const getAreaRect = (area: Area): AreaRect => areaMap[area].rect;

export const getAreaStyle = (area: Area): React.CSSProperties => {
  const meta = areaMap[area];
  return {
    backgroundColor: meta.backgroundColor,
    // backgroundImage: `url(...)` とかでもOK
  };
};

export const isInArea = (x: number, y: number, area: Area): boolean => {
  const rect = getAreaRect(area);
  return x >= rect.x && x < rect.x + rect.width && y >= rect.y && y < rect.y + rect.height;
};

export const getAreaByPosition = (x: number, y: number): Area | null => {
  return (Object.entries(areaMap) as [Area, AreaMeta][])  // ✅ ここを修正！
    .find(([area, _]) => isInArea(x, y, area))?.[0] ?? null;
};


export const getRandomPositionInArea = (area: Area): { x: number; y: number } => {
  const { x, y, width, height } = getAreaRect(area);
  return {
    x: Math.floor(x + Math.random() * (width - 32)),
    y: Math.floor(y + Math.random() * (height - 32)),
  };
};

// 📐 全体フィールドの最大サイズ（自動算出）
export const fieldWidth = Math.max(...Object.values(areaMap).map(a => a.rect.x + a.rect.width));
export const fieldHeight = Math.max(...Object.values(areaMap).map(a => a.rect.y + a.rect.height));
