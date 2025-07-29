import { useEffect } from 'react';
import { ellipsis } from '../../domain/utils/string'; 
import { UserModel } from '../../domain/user/UserModel';
import { useUserViewStore } from '../../infra/cache/UserViewStore';
import { Sprite } from '../../viewmodel/Sprite';
import { CommentBubble } from './CommentBubble';
import { Direction } from '../../domain/user/Direction';
import { UserState } from '../../domain/user/UserState';
import { getRandomPositionInArea } from '../../domain/area/Area';

type Props = { 
  user: UserModel;
};

export const UserCard = ({ user }: Props) => {
  const view = useUserViewStore((s) => s.getView(user.id));
  const clearExpired = useUserViewStore((s) => s.clearExpiredComments);

  // コメントクリア
  useEffect(() => {
    const timer = setInterval(clearExpired, 1000);
    return () => clearInterval(timer);
  }, [clearExpired]);

  // 初期位置設定
  useEffect(() => {
    if (view && !view.position) {
      const pos = getRandomPositionInArea(user.area);
      useUserViewStore.getState().setPosition(user.id, pos.x, pos.y);
    }
  }, [view, user.area, user.id]);

  if (!view) return null;
  const { x, y } = view.position;

  return (
    <div
      className="absolute pointer-events-none"
      style={{ left: x, top: y, zIndex: 50 }}
    >
      {/* コメントバブル(必要なら 0, -24 などでオフセット) */}
      {view.comment && (
        <div style={{ position: 'absolute', left: 0, top: -24, maxWidth: 120 }}>
          <CommentBubble comment={ellipsis(view.comment, 10)} />
        </div>
      )}

      {/* スプライト＋情報(スプライトは左上基準、情報は右へ12pxオフセット) */}
      <div
        className="flex items-center space-x-2 bg-white bg-opacity-90 p-1 rounded-lg shadow-md"
        style={{ position: 'absolute', left: 12, top: 0 }}
      >
        <div
          className={`w-8 h-8 ${
            user.state === UserState.Dancing ? 'animate-wiggle' : ''
          }`}
        >
          <Sprite
            direction={view.direction ?? Direction.Down}
            isWalking={user.state === UserState.Walking}
          />
        </div>
        <div className="text-sm text-gray-800 whitespace-nowrap">
          <p className="font-medium">{ellipsis(user.name, 5)}</p>
          <p className="text-xs">{ellipsis(user.work_name ?? '', 5)}</p>
        </div>
      </div>
    </div>
  );
};
