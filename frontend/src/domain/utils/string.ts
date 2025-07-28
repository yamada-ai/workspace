// utils/string.ts
/** 
 * maxLen文字まで表示し、超過する場合は末尾を「…」に置き換える
 * @param str 元の文字列
 * @param maxLen 最大文字数（省略記号含む）
 */
export function ellipsis(str: string, maxLen: number = 7): string {
    if (str.length <= maxLen) {
      return str;
    }
    // 先頭 (maxLen - 1) 文字 + 「…」
    return str.slice(0, maxLen - 1) + '…';
  }
  