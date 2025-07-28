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
      style={{ width: `${fieldWidth}px`, height: `${fieldHeight}px` }}
    >
      {Object.values(Area).map((area) => {
        const { x, y, width, height } = getAreaRect(area);
        const style = getAreaStyle(area);
        const usersInArea = getAllUsers().filter((u) => u.area === area);

        return (
          <div
            key={area}
            className="absolute border border-gray-500"
            style={{ left: x, top: y, width, height, ...style }}
          >
            <p className="text-xs text-center bg-white">{area}</p>

            {/* エリア内の相対コンテナは一度だけ */}
            <div className="relative w-full h-full">
              {usersInArea.map((u) => (
                <UserCard key={u.id} user={u} />
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
};
