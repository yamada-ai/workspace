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
        return (
          <div
            key={area}
            className="absolute border border-gray-500"
            style={{ left: x, top: y, width, height, ...style }}
          >
            <p className="text-xs text-center bg-white">{area}</p>
            {getAllUsers()
              .filter((u) => u.area === area)
              .map((u) => (
                <UserCard key={u.id} user={u} />
              ))}
          </div>
        );
      })}
    </div>
  );
};
