"use strict";
//From: https://github.com/KevinAdu/nengo
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.gregorianYearRange = exports.japaneseYear = void 0;
const periods_json_1 = __importDefault(require("./periods.json"));
/**
 * Converts Gregorian calendar year to Japanese calendar year
 */
const japaneseYear = gregorianDate => {
    const gregorianYear = gregorianDate.getFullYear();
    const gregorianMonth = gregorianDate.getMonth() + 1;
    const gregorianDay = gregorianDate.getDate();
    const periodsOrdered = periods_json_1.default.sort((a, b) => b.startYear - a.startYear);
    if (gregorianYear < periodsOrdered[periodsOrdered.length - 1].startYear)
        return undefined;
    const exactPeriod = periodsOrdered.find((period, i) => {
        if (i === periodsOrdered.length - 1)
            return true;
        if (gregorianYear > period.startYear)
            return true;
        if (gregorianYear === period.startYear &&
            gregorianMonth > period.startMonth) {
            return true;
        }
        if (gregorianYear === period.startYear &&
            gregorianMonth === period.startMonth &&
            gregorianDay >= period.startDay) {
            return true;
        }
        return false;
    });
    let updatedPeriod;
    if (exactPeriod) {
        updatedPeriod = Object.assign({ currentJapaneseYear: gregorianYear - exactPeriod.startYear + 1 }, exactPeriod);
    }
    return updatedPeriod;
};
exports.japaneseYear = japaneseYear;
/**
 * Converts Japanese calendar year to Gregorian year range
 * @param {String} year
 * @return {YearRange | undefined}
 */
const gregorianYearRange = (japanesePeriod) => {
    let yearRange = undefined;
    const foundPeriod = periods_json_1.default.find(period => period.names.kanji === japanesePeriod ||
        period.names.hiragana === japanesePeriod ||
        period.names.english === japanesePeriod);
    if (foundPeriod) {
        const previousPeriod = periods_json_1.default[periods_json_1.default.indexOf(foundPeriod) - 1];
        const previousYear = previousPeriod && previousPeriod.startYear - 1;
        yearRange = {
            startYear: foundPeriod.startYear,
            endYear: previousYear
        };
    }
    return yearRange;
};
exports.gregorianYearRange = gregorianYearRange;
