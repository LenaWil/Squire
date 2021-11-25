/**
 * Converts Gregorian calendar year to Japanese calendar year
 */
export declare const japaneseYear: JapaneseYearFunction;
/**
 * Converts Japanese calendar year to Gregorian year range
 * @param {String} year
 * @return {YearRange | undefined}
 */
export declare const gregorianYearRange: GregorianYearRangeFunction;

type Period = {
  startYear: number;
  startMonth: number;
  startDay: number;
  names: {
    kanji: string;
    hiragana: string;
    english: string;
  };
};

type PeriodAndExactYear =
  | Period & {
    currentJapaneseYear: number;
  }
  | undefined;

type YearRange = {
  startYear: number;
  endYear?: number;
};

type JapaneseYearFunction = (gregorianDate: Date) => PeriodAndExactYear;
type GregorianYearRangeFunction = (
  japanesePeriod: string
) => YearRange | undefined;
