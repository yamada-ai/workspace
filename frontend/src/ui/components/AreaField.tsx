import {
  Area,
  getAreaRect,
  getAreaStyle,
  fieldWidth,
  fieldHeight,
} from '../../domain/area/Area';
import { useUserStore } from '../../infra/cache/useUserStore';
import { UserCard } from './UserCard';

export const AreaField = () => {
  const getAllUsers = useUserStore((s) => s.getAllUsers);

  return (
    <div
      className="relative border border-gray-300"
      style={{ width: fieldWidth, height: fieldHeight }}
    >
      {Object.values(Area).map((area, idx) => {
        const { x, y, width, height } = getAreaRect(area);
        const style = getAreaStyle(area);
        const users = getAllUsers().filter((u) => u.area === area);

        return (
          <div
            key={area}
            className="absolute border border-gray-500 overflow-visible"
            style={{ left: x, top: y, width, height, zIndex: idx * 10, ...style }}
          >
            <p className="text-xs text-center bg-white">{area}</p>
            <div className="relative w-full h-full" style={{ zIndex: idx * 10 + 1 }}>
              {users.map((u) => (
                <UserCard key={u.id} user={u} />
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
};