type Props = {
    comment: string;
  };
  
  export const CommentBubble = ({ comment }: Props) => {
    return (
      <div className="comment-bubble">
        {comment}
      </div>
    );
  };
  