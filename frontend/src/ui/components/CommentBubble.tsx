  
export const CommentBubble = ({ comment }: { comment: string }) => (
  <span
    className="absolute -top-6 left-1/2 -translate-x-1/2 whitespace-nowrap
                 bg-white px-2 py-1 rounded text-sm shadow-md pointer-events-none z-10
                 animate-fadeInOut"
    >
    {comment}
  </span>
);